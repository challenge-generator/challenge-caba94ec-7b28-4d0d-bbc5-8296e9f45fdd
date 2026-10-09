import json
import logging
import threading
from typing import Callable, Optional
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import ValidationError

from app.infrastructure.messaging.event_serializer import EventSerializer
from app.domain.events import (
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    DomainEvent,
)

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """Consumidor de mensajes RabbitMQ para eventos de transacciones.
    
    Implementa patrón de reconnect automático y manejo de errores.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        queue_name: str = "transaction_events",
        exchange_name: str = "transactions",
        routing_key: str = "transaction.#",
        prefetch_count: int = 10,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.prefetch_count = prefetch_count
        
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[BlockingChannel] = None
        self._serializer = EventSerializer()
        self._consuming = False
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 5
        self._reconnect_delay = 5
        self._lock = threading.Lock()
        self._event_handler: Optional[Callable[[DomainEvent], None]] = None

    def connect(self) -> None:
        """Establece conexión con RabbitMQ."""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
            connection_attempts=3,
            retry_delay=1,
        )
        
        try:
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._setup_exchange_and_queue()
            self._channel.basic_qos(prefetch_count=self.prefetch_count)
            self._reconnect_attempts = 0
            logger.info(
                f"Conectado a RabbitMQ en {self.host}:{self.port}"
            )
        except Exception as e:
            logger.error(f"Error al conectar a RabbitMQ: {e}")
            self._handle_connection_error(e)
            raise

    def _setup_exchange_and_queue(self) -> None:
        """Configura el exchange, cola y bindings."""
        if not self._channel:
            raise RuntimeError("Canal no inicializado")
        
        self._channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type="topic",
            durable=True,
        )
        
        self._channel.queue_declare(
            queue=self.queue_name,
            durable=True,
            arguments={
                "x-message-ttl": 86400000,
                "x-dead-letter-exchange": f"{self.exchange_name}.dlx",
                "x-dead-letter-routing-key": "dead-letter",
            },
        )
        
        self._channel.queue_bind(
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key,
        )
        
        logger.info(
            f"Exchange '{self.exchange_name}' y cola '{self.queue_name}' configurados"
        )

    def register_handler(
        self, handler: Callable[[DomainEvent], None]
    ) -> None:
        """Registra el handler para procesar eventos."""
        self._event_handler = handler

    def start_consuming(self) -> None:
        """Inicia el consumo de mensajes."""
        if not self._channel:
            raise RuntimeError("Canal no inicializado. Llama a connect() primero.")
        
        self._consuming = True
        self._channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message,
            auto_ack=False,
        )
        
        logger.info(f"Iniciando consumo de '{self.queue_name}'...")
        
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Consumo interrumpido por usuario")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error en el ciclo de consumo: {e}")
            self._handle_connection_error(e)
            raise

    def _on_message(
        self,
        channel: BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        """Callback para procesar mensajes recibidos."""
        try:
            event = self._deserialize_message(body, properties)
            
            if self._event_handler:
                self._event_handler(event)
            
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.debug(f"Evento procesado: {event.event_type}")
            
        except ValidationError as e:
            logger.error(f"Error de validación del evento: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def _deserialize_message(
        self,
        body: bytes,
        properties: pika.spec.BasicProperties,
    ) -> DomainEvent:
        """Deserializa el mensaje según su tipo."""
        content_type = properties.content_type or "application/json"
        
        if content_type != "application/json":
            raise ValueError(f"Content type no soportado: {content_type}")
        
        message_data = json.loads(body.decode("utf-8"))
        event_type = message_data.get("event_type")
        
        return self._serializer.deserialize(message_data, event_type)

    def _handle_connection_error(self, error: Exception) -> None:
        """Maneja errores de conexión con reintentos."""
        with self._lock:
            if self._reconnect_attempts >= self._max_reconnect_attempts:
                logger.error(
                    f"Máximo de reintentos alcanzado. Error: {error}"
                )
                raise
            
            self._reconnect_attempts += 1
            logger.warning(
                f"Reintentando conexión ({self._reconnect_attempts}/{self._max_reconnect_attempts}) "
                f"en {self._reconnect_delay}s..."
            )

    def stop_consuming(self) -> None:
        """Detiene el consumo de mensajes."""
        self._consuming = False
        if self._channel and self._channel.is_open:
            self._channel.stop_consuming()
        logger.info("Consumo detenido")

    def close(self) -> None:
        """Cierra la conexión con RabbitMQ."""
        self.stop_consuming()
        
        if self._channel and self._channel.is_open:
            self._channel.close()
            logger.info("Canal de RabbitMQ cerrado")
        
        if self._connection and self._connection.is_open:
            self._connection.close()
            logger.info("Conexión a RabbitMQ cerrada")

    def __enter__(self) -> "RabbitMQConsumer":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()