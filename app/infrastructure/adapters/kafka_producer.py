import logging
import asyncio
from typing import Optional
from uuid import UUID

from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class KafkaProducerAdapter:
    """Adaptador para publicar eventos en Apache Kafka.
    
    Implementa el patrón de adaptador para el puerto EventPublisher.
    Maneja la serialización de eventos y la configuración de entrega
    con garantías de tolerancia a fallos.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._producer: Optional[Producer] = None
        self._topics = {
            EventType.TRANSACTION_INITIATED: settings.kafka_topic_transactions,
            EventType.TRANSACTION_COMPLETED: settings.kafka_topic_transactions,
            EventType.TRANSACTION_FAILED: settings.kafka_topic_transactions,
        }
        self._delivery_reports: dict = {}
        self._init_producer()
    
    def _init_producer(self) -> None:
        """Inicializa el productor de Kafka con configuración optimizada."""
        config = {
            'bootstrap.servers': self._settings.kafka_bootstrap_servers,
            'client.id': self._settings.kafka_client_id,
            'acks': self._settings.kafka_acks,
            'retries': self._settings.kafka_retries,
            'retry.backoff.ms': self._settings.kafka_retry_backoff_ms,
            'enable.idempotence': True,
            'max.in.flight.requests.per.connection': 5,
            'compression.type': 'lz4',
            'linger.ms': 5,
            'batch.size': 16384,
        }
        self._producer = Producer(config)
        logger.info(f"Productor Kafka inicializado hacia {self._settings.kafka_bootstrap_servers}")
    
    def _delivery_callback(self, err, msg) -> None:
        """Callback para reportes de entrega de mensajes."""
        if err is not None:
            logger.error(f"Error en entrega de mensaje: {err}")
            self._delivery_reports[msg.topic()] = {'success': False, 'error': str(err)}
        else:
            logger.debug(f"Mensaje entregado a {msg.topic()} [{msg.partition()}] offset {msg.offset()}")
            self._delivery_reports[msg.topic()] = {'success': True, 'offset': msg.offset()}
    
    async def publish(self, event: TransactionEvent) -> bool:
        """Publica un evento en el topic de Kafka correspondiente.
        
        Args:
            event: Evento de dominio a publicar.
            
        Returns:
            True si el evento se publicó exitosamente, False en caso contrario.
        """
        if self._producer is None:
            logger.error("Productor Kafka no inicializado")
            return False
        
        try:
            topic = self._topics.get(event.event_type)
            if not topic:
                logger.error(f"Topic no configurado para evento tipo {event.event_type}")
                return False
            
            message_key = event.transaction_id
            message_value = event.model_dump_json()
            
            self._producer.produce(
                topic=topic,
                key=message_key,
                value=message_value,
                callback=self._delivery_callback,
            )
            self._producer.poll(0)
            
            logger.info(f"Evento {event.event_type.value} publicado para transacción {message_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error publicando evento en Kafka: {e}")
            return False
    
    async def publish_batch(self, events: list[TransactionEvent]) -> int:
        """Publica un lote de eventos de forma eficiente.
        
        Args:
            events: Lista de eventos a publicar.
            
        Returns:
            Número de eventos publicados exitosamente.
        """
        success_count = 0
        for event in events:
            if await self.publish(event):
                success_count += 1
        
        self._producer.flush()
        logger.info(f"Publicados {success_count}/{len(events)} eventos del lote")
        return success_count
    
    async def create_topics(self) -> None:
        """Crea los topics de Kafka si no existen."""
        admin_client = AdminClient({
            'bootstrap.servers': self._settings.kafka_bootstrap_servers
        })
        
        topics_to_create = [
            NewTopic(
                self._settings.kafka_topic_transactions,
                num_partitions=self._settings.kafka_num_partitions,
                replication_factor=self._settings.kafka_replication_factor,
            ),
        ]
        
        try:
            fs = admin_client.create_topics(topics_to_create, validate_only=True)
            for topic, f in fs.items():
                try:
                    f.result()
                    logger.info(f"Topic {topic} creado o ya existe")
                except Exception as e:
                    logger.warning(f"Error creando topic {topic}: {e}")
        except Exception as e:
            logger.error(f"Error en admin de Kafka: {e}")
    
    def flush(self, timeout: float = 10.0) -> None:
        """Fuerza el flush de mensajes pendientes.
        
        Args:
            timeout: Tiempo máximo de espera en segundos.
        """
        if self._producer:
            remaining = self._producer.flush(timeout)
            if remaining > 0:
                logger.warning(f"{remaining} mensajes pendientes tras flush")
    
    def close(self) -> None:
        """Cierra el productor y libera recursos."""
        self.flush()
        if self._producer:
            self._producer = None
            logger.info("Productor Kafka cerrado")