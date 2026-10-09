"""
Puerto para el consumo de eventos del dominio.
Define el contrato que la infraestructura debe implementar para suscribirse
y procesar eventos desde sistemas de mensajería como Kafka, RabbitMQ o SQS.
"""
from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Optional
from uuid import UUID

from app.domain.events import TransactionEvent, TransactionInitiated, TransactionCompleted, TransactionFailed


EventHandler = Callable[[TransactionEvent], Awaitable[None]]
"""
Tipo que define un handler de evento.
Cada handler procesa un evento de dominio específico.
"""


class MessageProcessingResult:
    """
    Resultado del procesamiento de un mensaje.
    Permite trackear el estado y metadatos del procesamiento.
    """
    
    def __init__(
        self,
        success: bool,
        event_id: Optional[UUID] = None,
        error_message: Optional[str] = None,
        retry_count: int = 0
    ):
        self.success = success
        self.event_id = event_id
        self.error_message = error_message
        self.retry_count = retry_count
        
    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"<MessageProcessingResult {status} event_id={self.event_id} retries={self.retry_count}>"


class EventConsumer(ABC):
    """
    Interfaz abstracta para consumir eventos del dominio.
    
    La implementación concreta (Kafka, RabbitMQ, SQS) será inyectada
    y procesará eventos según la configuración del sistema.
    """

    @abstractmethod
    async def subscribe_to_transaction_initiated(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción iniciada.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe_to_transaction_completed(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción completada.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe_to_transaction_failed(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción fallida.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        topic: str,
        handler: EventHandler,
        event_type_filter: Optional[type[TransactionEvent]] = None
    ) -> None:
        """
        Suscribe un handler genérico a un topic.
        
        Args:
            topic: Topic o cola a escuchar.
            handler: Función que procesa cualquier evento recibido.
            event_type_filter: Filtro opcional por tipo de evento.
        """
        pass

    @abstractmethod
    async def start_consuming(self) -> None:
        """
        Inicia el consumo de mensajes.
        Bloquea hasta que se detenga el consumidor.
        """
        pass

    @abstractmethod
    async def stop_consuming(self) -> None:
        """
        Detiene el consumo de mensajes de manera graceful.
        Procesa los mensajes en flight antes de cerrar.
        """
        pass

    @abstractmethod
    async def process_message(
        self,
        raw_message: bytes,
        handler: EventHandler
    ) -> MessageProcessingResult:
        """
        Procesa un mensaje raw deserializándolo y ejecutando el handler.
        
        Args:
            raw_message: Mensaje en bytes del broker de mensajería.
            handler: Handler a ejecutar con el evento deserializado.
            
        Returns:
            Resultado del procesamiento con éxito/fracaso y metadatos.
        """
        pass

    @abstractmethod
    def is_consuming(self) -> bool:
        """
        Verifica si el consumidor está activo.
        
        Returns:
            True si está consumiendo mensajes, False si está detenido.
        """
        pass

    @abstractmethod
    async def get_consumer_stats(self) -> dict:
        """
        Obtiene estadísticas del consumidor para monitoreo.
        
        Returns:
            Diccionario con métricas: mensajes procesados, errores, latencia, etc.
        """
        pass