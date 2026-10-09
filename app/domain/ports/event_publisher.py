"""
Puerto para la publicación de eventos del dominio.
Define el contrato que la infraestructura debe implementar para emitir
eventos a sistemas de mensajería como Kafka, RabbitMQ o SQS.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.events import TransactionEvent, TransactionInitiated, TransactionCompleted, TransactionFailed


class EventPublisher(ABC):
    """
    Interfaz abstracta para publicar eventos del dominio.
    
    La implementación concreta será inyectada por el contenedor de dependencias
    y puede variar según el entorno (desarrollo, testing, producción).
    """

    @abstractmethod
    async def publish_transaction_initiated(
        self,
        event: TransactionInitiated,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción iniciada.
        
        Args:
            event: Evento de dominio con los datos de la transacción.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish_transaction_completed(
        self,
        event: TransactionCompleted,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción completada.
        
        Args:
            event: Evento de dominio con los datos de la transacción completada.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish_transaction_failed(
        self,
        event: TransactionFailed,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción fallida.
        
        Args:
            event: Evento de dominio con los datos del fallo.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish(
        self,
        event: TransactionEvent,
        topic: str,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento genérico al topic especificado.
        
        Args:
            event: Cualquier evento de transacción del dominio.
            topic: Nombre del topic o cola de destino.
            idempotency_key: Clave para garantizar idempotencia.
            
        Returns:
            True si el evento fue publicado exitosamente.
        """
        pass

    @abstractmethod
    async def publish_batch(
        self,
        events: list[TransactionEvent],
        topic: str,
        idempotency_key_prefix: Optional[str] = None
    ) -> list[bool]:
        """
        Publica un lote de eventos de manera eficiente.
        
        Optimizado para alto throughput (5000 TPS objetivo).
        
        Args:
            events: Lista de eventos a publicar.
            topic: Nombre del topic o cola de destino.
            idempotency_key_prefix: Prefijo para generar claves de idempotencia.
            
        Returns:
            Lista de booleanos indicando éxito o fracaso de cada publicación.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Cierra las conexiones y libera recursos del publisher.
        Debe ser llamado al shutting down de la aplicación.
        """
        pass