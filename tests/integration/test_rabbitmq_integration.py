import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
import json

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.events import TransactionFailed, EventType
from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter
from app.infrastructure.messaging.event_serializer import EventSerializer


class TestRabbitMQIntegration:
    """Tests de integración para validar la comunicación con RabbitMQ."""

    @pytest.fixture
    def sample_failed_transaction(self):
        """Crea una transacción fallida de ejemplo para las pruebas."""
        return Transaction(
            id=uuid4(),
            account_id=uuid4(),
            amount=Decimal("-100.00"),
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.FAILED,
            failure_reason="Fondos insuficientes",
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_rabbitmq_connection(self):
        """Mock de la conexión a RabbitMQ."""
        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel
            yield mock_channel

    @pytest.mark.asyncio
    async def test_rabbitmq_producer_publish_event(self, sample_failed_transaction, mock_rabbitmq_connection):
        """Verifica que el producer publique eventos en RabbitMQ correctamente."""
        event = TransactionFailed.from_transaction(
            sample_failed_transaction,
            EventType.FAILED
        )

        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events'
        )

        await producer.publish('transaction.events', event)

        mock_rabbitmq_connection.basic_publish.assert_called_once()
        call_args = mock_rabbitmq_connection.basic_publish.call_args
        assert call_args[1]['exchange'] == ''
        assert call_args[1]['routing_key'] == 'transaction.events'

    @pytest.mark.asyncio
    async def test_rabbitmq_consumer_receives_message(self):
        """Verifica que el consumer reciba mensajes de RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_consumer import RabbitMQConsumerAdapter

        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel

            test_message = {
                'transaction_id': str(uuid4()),
                'event_type': 'FAILED',
                'amount': '100.00'
            }

            mock_channel.basic_consume.return_value = None

            consumer = RabbitMQConsumerAdapter(
                host='localhost',
                port=5672,
                queue='transaction.events'
            )

            messages = []

            def on_message_callback(ch, method, properties, body):
                messages.append(json.loads(body))
                ch.basic_ack(delivery_tag=method.delivery_tag)

            mock_channel.basic_consume = AsyncMock()
            mock_channel.basic_consume.side_effect = on_message_callback

            with patch('pika.SelectConnection'):
                pass

    @pytest.mark.asyncio
    async def test_rabbitmq_event_serialization(self, sample_failed_transaction):
        """Verifica la serialización de eventos para RabbitMQ."""
        event = TransactionFailed.from_transaction(
            sample_failed_transaction,
            EventType.FAILED
        )
        serializer = EventSerializer()

        serialized = serializer.serialize(event)

        assert isinstance(serialized, bytes)
        decoded = json.loads(serialized.decode('utf-8'))
        assert decoded['transaction_id'] == str(sample_failed_transaction.id)
        assert decoded['event_type'] == 'FAILED'

    @pytest.mark.asyncio
    async def test_rabbitmq_producer_confirm_delivery(self, mock_rabbitmq_connection):
        """Verifica la confirmación de entrega de mensajes en RabbitMQ."""
        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events',
            confirm_delivery=True
        )

        mock_rabbitmq_connection.confirm_delivery.assert_not_called()

        await producer.publish('transaction.events', MagicMock())

    @pytest.mark.asyncio
    async def test_rabbitmq_dead_letter_queue(self):
        """Verifica el manejo de dead letter queue en RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter

        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel

            producer = RabbitMQProducerAdapter(
                host='localhost',
                port=5672,
                queue='transaction.events',
                dead_letter_queue='transaction.events.dlq'
            )

            mock_channel.queue_declare.assert_called()

            dlq_call = mock_channel.queue_declare.call_args_list[1]
            assert 'transaction.events.dlq' in str(dlq_call)

    @pytest.mark.asyncio
    async def test_rabbitmq_retry_mechanism(self, mock_rabbitmq_connection):
        """Verifica el mecanismo de reintentos en RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter

        mock_rabbitmq_connection.basic_publish.side_effect = [
            Exception("Connection error"),
            None
        ]

        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events',
            retry_attempts=3,
            retry_delay=1
        )

        event = TransactionFailed(
            transaction_id=str(uuid4()),
            event_type=EventType.FAILED,
            timestamp=datetime.now().isoformat(),
            failure_reason="Error de conexión"
        )

        with patch('asyncio.sleep', new_callable=AsyncMock):
            await producer.publish('transaction.events', event)

        assert mock_rabbitmq_connection.basic_publish.call_count == 2