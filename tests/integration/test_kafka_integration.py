import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
import json

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.events import TransactionInitiated, TransactionCompleted, EventType
from app.infrastructure.adapters.kafka_producer import KafkaProducerAdapter
from app.infrastructure.messaging.event_serializer import EventSerializer


class TestKafkaIntegration:
    """Tests de integración para validar la comunicación con Kafka."""

    @pytest.fixture
    def sample_transaction(self):
        """Crea una transacción de ejemplo para las pruebas."""
        return Transaction(
            id=uuid4(),
            account_id=uuid4(),
            amount=Decimal("500.00"),
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_kafka_producer(self):
        """Mock del producer de Kafka."""
        with patch('confluent_kafka.Producer') as mock_prod:
            mock_instance = MagicMock()
            mock_prod.return_value = mock_instance
            yield mock_instance

    @pytest.mark.asyncio
    async def test_kafka_producer_publish_event(self, sample_transaction, mock_kafka_producer):
        """Verifica que el producer publique eventos en Kafka correctamente."""
        event = TransactionInitiated.from_transaction(sample_transaction, EventType.INITIATED)
        serializer = EventSerializer()
        serialized = serializer.serialize(event)

        producer = KafkaProducerAdapter(
            bootstrap_servers='localhost:9092',
            topic='transaction.events'
        )

        await producer.publish('transaction.events', event)

        mock_kafka_producer.produce.assert_called_once()
        call_args = mock_kafka_producer.produce.call_args
        assert call_args[1]['topic'] == 'transaction.events'

    @pytest.mark.asyncio
    async def test_kafka_consumer_receives_message(self):
        """Verifica que el consumer reciba mensajes de Kafka."""
        from app.infrastructure.adapters.kafka_consumer import KafkaConsumerAdapter

        with patch('confluent_kafka.Consumer') as mock_cons:
            mock_instance = MagicMock()
            mock_cons.return_value = mock_instance

            mock_message = MagicMock()
            mock_message.value.return_value = json.dumps({
                'transaction_id': str(uuid4()),
                'event_type': 'INITIATED',
                'amount': '500.00'
            }).encode('utf-8')
            mock_message.error.return_value = None

            mock_instance.consume.return_value = [mock_message]

            consumer = KafkaConsumerAdapter(
                bootstrap_servers='localhost:9092',
                topic='transaction.events',
                group_id='test-group'
            )

            messages = []
            async for msg in consumer.consume():
                messages.append(msg)
                if len(messages) >= 1:
                    break

            assert len(messages) == 1

    @pytest.mark.asyncio
    async def test_kafka_event_serialization(self, sample_transaction):
        """Verifica la serialización de eventos para Kafka."""
        event = TransactionInitiated.from_transaction(sample_transaction, EventType.INITIATED)
        serializer = EventSerializer()

        serialized = serializer.serialize(event)

        assert isinstance(serialized, bytes)
        assert 'transaction_id' in serialized.decode('utf-8')
        assert 'event_type' in serialized.decode('utf-8')

        deserialized = serializer.deserialize(serialized)
        assert deserialized.transaction_id == str(sample_transaction.id)

    @pytest.mark.asyncio
    async def test_kafka_producer_error_handling(self, mock_kafka_producer):
        """Verifica el manejo de errores del producer de Kafka."""
        mock_kafka_producer.produce.side_effect = Exception("Kafka broker unavailable")

        producer = KafkaProducerAdapter(
            bootstrap_servers='localhost:9092',
            topic='transaction.events'
        )

        event = TransactionInitiated(
            transaction_id=str(uuid4()),
            event_type=EventType.INITIATED,
            timestamp=datetime.now().isoformat()
        )

        with pytest.raises(Exception):
            await producer.publish('transaction.events', event)

    @pytest.mark.asyncio
    async def test_kafka_idempotent_producer(self, sample_transaction):
        """Verifica la idempotencia del producer de Kafka."""
        from app.infrastructure.adapters.kafka_producer import KafkaProducerAdapter

        with patch('confluent_kafka.Producer') as mock_prod:
            mock_instance = MagicMock()
            mock_prod.return_value = mock_instance

            producer = KafkaProducerAdapter(
                bootstrap_servers='localhost:9092',
                topic='transaction.events',
                enable_idempotence=True
            )

            event = TransactionCompleted.from_transaction(sample_transaction, EventType.COMPLETED)

            await producer.publish('transaction.events', event)
            await producer.publish('transaction.events', event)

            assert mock_instance.produce.call_count == 2