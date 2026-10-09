import logging
import asyncio
from typing import Optional, Callable, Awaitable
from uuid import UUID

from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class MessageHandler:
    """Interfaz para manejar mensajes procesados."""
    
    async def handle(self, event: TransactionEvent) -> None:
        """Procesa un evento de transacción."""
        raise NotImplementedError


class KafkaConsumerAdapter:
    """Adaptador para consumir eventos desde Apache Kafka.
    
    Implementa el patrón de adaptador para el puerto EventConsumer.
    Maneja la deserialización de eventos, manejo de offsets y
    rebalanceo de particiones.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._consumer: Optional[Consumer] = None
        self._running = False
        self._handlers: dict[EventType, MessageHandler] = {}
        self._init_consumer()
    
    def _init_consumer(self) -> None:
        """Inicializa el consumidor de Kafka con configuración de alto throughput."""
        config = {
            'bootstrap.servers': self._settings.kafka_bootstrap_servers,
            'group.id': self._settings.kafka_consumer_group,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'auto.commit.interval.ms': 5000,
            'max.poll.interval.ms': 300000,
            'session.timeout.ms': 10000,
            'heartbeat.interval.ms': 3000,
            'fetch.min.bytes': 1,
            'fetch.max.wait.ms': 500,
            'max.partition.fetch.bytes': 1048576,
        }
        self._consumer = Consumer(config)
        logger.info(f"Consumidor Kafka inicializado para grupo {self._settings.kafka_consumer_group}")
    
    def register_handler(self, event_type: EventType, handler: MessageHandler) -> None:
        """Registra un handler para un tipo de evento específico.
        
        Args:
            event_type: Tipo de evento a manejar.
            handler: Instancia que procesará el evento.
        """
        self._handlers[event_type] = handler
        logger.info(f"Handler registrado para evento {event_type.value}")
    
    def _deserialize_event(self, message) -> Optional[TransactionEvent]:
        """Deserializa un mensaje de Kafka en un evento de dominio.
        
        Args:
            message: Mensaje raw de Kafka.
            
        Returns:
            Evento de dominio o None si la deserialización falla.
        """
        try:
            event_data = message.value().decode('utf-8')
            event_dict = TransactionEvent.model_validate_json(event_data)
            
            event_type = event_dict.event_type
            if event_type == EventType.TRANSACTION_INITIATED:
                return TransactionInitiated.model_validate_json(event_data)
            elif event_type == EventType.TRANSACTION_COMPLETED:
                return TransactionCompleted.model_validate_json(event_data)
            elif event_type == EventType.TRANSACTION_FAILED:
                return TransactionFailed.model_validate_json(event_data)
            else:
                logger.warning(f"Tipo de evento desconocido: {event_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error deserializando evento: {e}")
            return None
    
    async def _process_message(self, message) -> None:
        """Procesa un mensaje individual del topic.
        
        Args:
            message: Mensaje de Kafka a procesar.
        """
        event = self._deserialize_event(message)
        if event is None:
            logger.warning("Evento no deserializado, saltando mensaje")
            return
        
        handler = self._handlers.get(event.event_type)
        if handler is None:
            logger.debug(f"No hay handler para evento tipo {event.event_type.value}")
            return
        
        try:
            await handler.handle(event)
            logger.info(f"Evento {event.event_type.value} procesado para transacción {event.transaction_id}")
        except Exception as e:
            logger.error(f"Error procesando evento: {e}")
            raise
    
    async def start_consuming(self) -> None:
        """Inicia el loop de consumo de mensajes."""
        if self._consumer is None:
            logger.error("Consumidor Kafka no inicializado")
            return
        
        self._consumer.subscribe([self._settings.kafka_topic_transactions])
        self._running = True
        
        logger.info(f"Iniciando consumo del topic {self._settings.kafka_topic_transactions}")
        
        while self._running:
            try:
                msg = self._consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(f"Fin de partición {msg.partition()}")
                        continue
                    else:
                        logger.error(f"Error de Kafka: {msg.error()}")
                        continue
                
                await self._process_message(msg)
                
                self._consumer.commit(asynchronous=False)
                
            except KafkaException as e:
                logger.error(f"Excepción de Kafka: {e}")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error en loop de consumo: {e}")
                await asyncio.sleep(1)
    
    def stop_consuming(self) -> None:
        """Detiene el consumo de mensajes."""
        self._running = False
        logger.info("Consumidor Kafka deteniendo consumo")
    
    def close(self) -> None:
        """Cierra el consumidor y libera recursos."""
        self.stop_consuming()
        if self._consumer:
            self._consumer.close()
            self._consumer = None
            logger.info("Consumidor Kafka cerrado")
    
    async def get_partition_info(self, topic: str) -> dict:
        """Obtiene información de particiones para un topic.
        
        Args:
            topic: Nombre del topic.
            
        Returns:
            Diccionario con información de particiones.
        """
        admin_client = AdminClient({
            'bootstrap.servers': self._settings.kafka_bootstrap_servers
        })
        
        cluster_metadata = admin_client.list_topics(topic=topic, timeout=10)
        partitions_info = {}
        
        if topic in cluster_metadata.topics:
            topic_metadata = cluster_metadata.topics[topic]
            for partition in topic_metadata.partitions.values():
                partitions_info[partition.id] = {
                    'leader': partition.leader,
                    'replicas': partition.replicas,
                    'isrs': partition.isrs,
                }
        
        return partitions_info