import logging
import json
import pika
from typing import Optional
from uuid import UUID

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class RabbitMQProducerAdapter:
    """Adaptador para publicar mensajes en RabbitMQ.
    
    Implementa el patrón de adaptador para publicar eventos en colas
    de RabbitMQ. Utiliza confirmación de publicación y manejo de
    conexiones para garantizar la entrega.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
        self._exchanges = {
            EventType.TRANSACTION_INITIATED: settings.rabbitmq_exchange_transactions,
            EventType.TRANSACTION_COMPLETED: settings.rabbitmq_exchange_transactions,
            EventType.TRANSACTION_FAILED: settings.rabbitmq_exchange_transactions,
        }
        self._init_connection()
    
    def _init_connection(self) -> None:
        """Inicializa la conexión a RabbitMQ con configuración robusta."""
        credentials = pika.PlainCredentials(
            self._settings.rabbitmq_username,
            self._settings.rabbitmq_password,
        )
        
        parameters = pika.ConnectionParameters(
            host=self._settings.rabbitmq_host,
            port=self._settings.rabbitmq_port,
            virtual_host=self._settings.rabbitmq_vhost,
            credentials=credentials,
            connection_attempts=3,
            retry_delay=1,
            socket_timeout=5,
            heartbeat=60,
            blocked_connection_timeout=300,
        )
        
        try:
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._channel.confirm_delivery()
            self._declare_exchanges_and_queues()
            logger.info(f"Conexión RabbitMQ establecida hacia {self._settings.rabbitmq_host}:{self._settings.rabbitmq_port}")
        except Exception as e:
            logger.error(f"Error conectando a RabbitMQ: {e}")
            raise
    
    def _declare_exchanges_and_queues(self) -> None:
        """Declara los exchanges y colas necesarios."""
        if self._channel is None:
            return
        
        self._channel.exchange_declare(
            exchange=self._settings.rabbitmq_exchange_transactions,
            exchange_type='topic',
            durable=True,
            auto_delete=False,
        )
        
        for event_type in EventType:
            queue_name = f"{self._settings.rabbitmq_queue_prefix}{event_type.value}"
            routing_key = event_type.value
            
            self._channel.queue_declare(
                queue=queue_name,
                durable=True,
                exclusive=False,
                auto_delete=False,
            )
            
            self._channel.queue_bind(
                exchange=self._settings.rabbitmq_exchange_transactions,
                queue=queue_name,
                routing_key=routing_key,
            )
            
            logger.info(f"Cola {queue_name} vinculada al exchange con routing key {routing_key}")
    
    def _serialize_event(self, event: TransactionEvent) -> str:
        """Serializa un evento a JSON para transmisión.
        
        Args:
            event: Evento de dominio a serializar.
            
        Returns:
            Representación JSON del evento.
        """
        return event.model_dump_json()
    
    def _on_publish_confirmation(self, method) -> None:
        """Callback para confirmaciones de publicación.
        
        Args:
            method: Método de confirmación de RabbitMQ.
        """
        if method.reply_code == 200:
            logger.debug(f"Publicación confirmada: {method.reply_code}")
        else:
            logger.warning(f"Publicación no confirmada: {method.reply_code} - {method.reply_text}")
    
    async def publish(self, event: TransactionEvent) -> bool:
        """Publica un evento en RabbitMQ.
        
        Args:
            event: Evento de dominio a publicar.
            
        Returns:
            True si el evento se publicó exitosamente, False en caso contrario.
        """
        if self._channel is None or self._connection is None or self._connection.is_closed:
            logger.error("Conexión RabbitMQ no disponible")
            self._reconnect()
            return False
        
        try:
            exchange = self._exchanges.get(event.event_type)
            routing_key = event.event_type.value
            message_body = self._serialize_event(event)
            
            properties = pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2,
                message_id=event.transaction_id,
                timestamp=int(event.occurred_at.timestamp()) if event.occurred_at else None,
                headers={
                    'event_type': event.event_type.value,
                    'transaction_id': str(event.transaction_id),
                },
            )
            
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message_body,
                properties=properties,
                mandatory=True,
            )
            
            logger.info(f"Evento {event.event_type.value} publicado para transacción {event.transaction_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error publicando en RabbitMQ: {e}")
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
        
        logger.info(f"Publicados {success_count}/{len(events)} eventos del lote")
        return success_count
    
    def _reconnect(self) -> None:
        """Reconecta a RabbitMQ si la conexión se perdió."""
        try:
            if self._connection and not self._connection.is_closed:
                self._connection.close()
            self._init_connection()
            logger.info("Reconexión a RabbitMQ exitosa")
        except Exception as e:
            logger.error(f"Error en reconexión: {e}")
    
    def close(self) -> None:
        """Cierra la conexión y libera recursos."""
        if self._channel:
            try:
                self._channel.close()
            except Exception:
                pass
            self._channel = None
        
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
        
        logger.info("Conexión RabbitMQ cerrada")