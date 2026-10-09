import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.domain.entities.transaction import Transaction, TransactionStatus
from app.domain.events import (
    DomainEvent,
    TransactionCompleted,
    TransactionEvent,
    TransactionFailed,
    TransactionInitiated,
)
from app.domain.ports.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)


class TransactionEventHandler:
    """
    Manejador de eventos para procesar eventos entrantes del sistema EDA.
    Actualiza el estado de las transacciones y coordina flujos derivados.
    """

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher,  # EventPublisher del dominio
    ):
        self._repository = transaction_repository
        self._event_publisher = event_publisher

    async def handle_transaction_initiated(
        self, event: TransactionInitiated
    ) -> None:
        """
        Procesa el evento de transacción iniciada.
        Puede iniciar verificaciones adicionales o flujos derivados.

        Args:
            event: Evento de transacción iniciada
        """
        logger.info(
            f"Manejando TransactionInitiated para {event.transaction_id}"
        )

        # Buscar la transacción
        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.warning(
                f"Transacción {event.transaction_id} no encontrada para evento"
            )
            return

        # Verificar que el estado sea consistente
        if transaction.status != TransactionStatus.PENDING:
            logger.warning(
                f"Transacción {event.transaction_id} en estado inesperado: {transaction.status}"
            )
            return

        # Aquí se pueden lanzar flujos derivados:
        # - Notificaciones al usuario
        # - Verificaciones de fraude
        # - Reservas de fondos
        # Por ahora, solo registramos el procesamiento
        logger.debug(
            f"Evento TransactionInitiated procesado para {event.transaction_id}"
        )

    async def handle_transaction_completed(
        self, event: TransactionCompleted
    ) -> None:
        """
        Procesa el evento de transacción completada.
        Actualiza el estado y puede iniciar flujos post-completación.

        Args:
            event: Evento de transacción completada
        """
        logger.info(
            f"Manejando TransactionCompleted para {event.transaction_id}"
        )

        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.error(
                f"Transacción {event.transaction_id} no encontrada para completación"
            )
            return

        # Actualizar estado en repositorio
        await self._repository.update_status(
            event.transaction_id, TransactionStatus.COMPLETED.value
        )

        # Post-procesamiento: notificaciones, sincronización, etc.
        await self._trigger_post_completion_actions(transaction)

        logger.info(
            f"Transacción {event.transaction_id} procesada completamente"
        )

    async def handle_transaction_failed(
        self, event: TransactionFailed
    ) -> None:
        """
        Procesa el evento de transacción fallida.
        Registra la falla y puede iniciar flujos de compensación.

        Args:
            event: Evento de transacción fallida
        """
        logger.warning(
            f"Manejando TransactionFailed para {event.transaction_id}: {event.failure_reason}"
        )

        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.error(
                f"Transacción {event.transaction_id} no encontrada para manejo de falla"
            )
            return

        # Actualizar estado a fallido
        await self._repository.update_status(
            event.transaction_id, TransactionStatus.FAILED.value
        )

        # Acciones de compensación: liberar fondos, notificar al usuario, etc.
        await self._trigger_compensation_actions(transaction, event.failure_reason)

        logger.info(
            f"Transacción {event.transaction_id} marcada como fallida"
        )

    async def handle_event(self, event: DomainEvent) -> None:
        """
        Dispatcher principal que redirige al handler apropiado según el tipo de evento.

        Args:
            event: Evento de dominio a procesar
        """
        if isinstance(event, TransactionInitiated):
            await self.handle_transaction_initiated(event)
        elif isinstance(event, TransactionCompleted):
            await self.handle_transaction_completed(event)
        elif isinstance(event, TransactionFailed):
            await self.handle_transaction_failed(event)
        else:
            logger.warning(f"Tipo de evento no manejado: {type(event)}")

    async def _trigger_post_completion_actions(
        self, transaction: Transaction
    ) -> None:
        """
        Ejecuta acciones derivadas después de una transacción completada.
        Ejemplo: notificaciones, actualización de balances, etc.
        """
        # Simular acciones post-completación
        logger.debug(
            f"Ejecutando acciones post-completación para {transaction.id}"
        )

        # En implementación real:
        # - Notificar al usuario via email/push
        # - Actualizar balance de cuenta
        # - Generar comprobante
        # - Integrar con sistema contable

    async def _trigger_compensation_actions(
        self, transaction: Transaction, failure_reason: str
    ) -> None:
        """
        Ejecuta acciones de compensación cuando una transacción falla.

        Args:
            transaction: Transacción que falló
            failure_reason: Razón de la falla
        """
        logger.debug(
            f"Ejecutando acciones de compensación para {transaction.id}"
        )

        # En implementación real:
        # - Liberar fondos reservados
        # - Notificar al usuario del fracaso
        # - Registrar en log de auditoría
        # - Integrar con sistema de alertas

    async def get_pending_transactions(self) -> list[Transaction]:
        """
        Recupera todas las transacciones pendientes para monitoreo.

        Returns:
            Lista de transacciones en estado PENDING
        """
        return await self._repository.find_by_status(TransactionStatus.PENDING.value)

    async def recover_stale_transactions(self, max_age_minutes: int = 30) -> int:
        """
        Recupera transacciones que quedaron en estado PENDING por mucho tiempo.

        Args:
            max_age_minutes: Antigüedad máxima en minutos

        Returns:
            Cantidad de transacciones recuperadas
        """
        pending = await self.get_pending_transactions()
        recovered_count = 0

        now = datetime.now(timezone.utc)
        for txn in pending:
            age = (now - txn.updated_at).total_seconds() / 60
            if age > max_age_minutes:
                logger.info(
                    f"Recuperando transacción estancada {txn.id} (edad: {age:.1f} min)"
                )
                # Marcar como fallida por timeout
                await self._repository.update_status(
                    txn.id, TransactionStatus.FAILED.value
                )
                recovered_count += 1

        return recovered_count

    async def replay_event(self, event: TransactionEvent) -> bool:
        """
        Reproduce un evento para recuperación o debugging.

        Args:
            event: Evento a reproducir

        Returns:
            True si se procesó correctamente
        """
        logger.info(f"Reproduciendo evento {event.event_id}")
        try:
            await self.handle_event(event)
            return True
        except Exception as e:
            logger.error(f"Error reproduciendo evento {event.event_id}: {e}")
            return False