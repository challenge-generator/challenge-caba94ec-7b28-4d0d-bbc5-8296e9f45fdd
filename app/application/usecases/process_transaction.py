import logging
import uuid
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import ValidationError

from app.domain.entities.transaction import (
    Transaction,
    TransactionStatus,
    TransactionType,
)
from app.domain.events import (
    DomainEvent,
    TransactionCompleted,
    TransactionEvent,
    TransactionFailed,
    TransactionInitiated,
)
from app.domain.ports.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)


class ProcessTransactionUseCase:
    """
    Caso de uso principal para procesar transacciones financieras.
    Coordina la lógica de negocio y la emisión de eventos hacia la infraestructura.
    """

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher,  # EventPublisher del dominio (sin definición de firma visible)
    ):
        self._repository = transaction_repository
        self._event_publisher = event_publisher

    async def execute(
        self,
        account_id: UUID,
        amount: float,
        transaction_type: TransactionType,
        description: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Transaction:
        """
        Ejecuta el procesamiento de una nueva transacción.

        Args:
            account_id: ID de la cuenta origen
            amount: Monto de la transacción
            transaction_type: Tipo de transacción (DEBIT o CREDIT)
            description: Descripción opcional
            idempotency_key: Clave de idempotencia para evitar duplicados

        Returns:
            Transaction: La transacción procesada

        Raises:
            ValueError: Si los parámetros son inválidos
            RuntimeError: Si ocurre un error inesperado
        """
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a cero")

        if not account_id:
            raise ValueError("El account_id es obligatorio")

        # Verificar idempotencia
        if idempotency_key:
            existing = await self._find_by_idempotency_key(idempotency_key)
            if existing:
                logger.info(
                    f"Transacción duplicada detectada: {idempotency_key}"
                )
                return existing

        # Crear la transacción
        transaction = Transaction(
            id=uuid.uuid4(),
            account_id=account_id,
            amount=amount,
            type=transaction_type,
            status=TransactionStatus.PENDING,
            description=description or f"{transaction_type.value} transaction",
            idempotency_key=idempotency_key,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        try:
            # Persistir la transacción
            await self._repository.save(transaction)
            logger.info(f"Transacción {transaction.id} guardada en estado PENDING")

            # Emitir evento de transacción iniciada
            await self._emit_event(
                TransactionInitiated.from_transaction(
                    transaction,
                    "TRANSACTION_INITIATED",
                )
            )

            # Procesar la lógica de negocio
            processed_transaction = await self._process_transaction_logic(
                transaction
            )

            # Actualizar el estado según el resultado
            if processed_transaction.status == TransactionStatus.COMPLETED:
                processed_transaction.complete()
                await self._emit_event(
                    TransactionCompleted.from_transaction(
                        processed_transaction,
                        "TRANSACTION_COMPLETED",
                    )
                )
            elif processed_transaction.status == TransactionStatus.FAILED:
                processed_transaction.fail(
                    processed_transaction.description or "Unknown error"
                )
                await self._emit_event(
                    TransactionFailed.from_transaction(
                        processed_transaction,
                        "TRANSACTION_FAILED",
                    )
                )

            # Persistir el estado final
            await self._repository.update_status(
                processed_transaction.id,
                processed_transaction.status.value,
            )

            logger.info(
                f"Transacción {processed_transaction.id} completada con estado {processed_transaction.status.value}"
            )
            return processed_transaction

        except Exception as e:
            logger.error(f"Error procesando transacción: {e}")
            transaction.fail(str(e))
            await self._repository.update_status(
                transaction.id, TransactionStatus.FAILED.value
            )
            await self._emit_event(
                TransactionFailed.from_transaction(transaction, "TRANSACTION_FAILED")
            )
            raise

    async def _process_transaction_logic(self, transaction: Transaction) -> Transaction:
        """
        Procesa la lógica de negocio específica de la transacción.
        En una implementación real, esto invocaría servicios externos,
        validaciones adicionales, etc.
        """
        # Simular procesamiento
        # En producción: llamar a servicios de verificación, Scoring, etc.
        try:
            # Lógica de validación de negocio
            if transaction.type == TransactionType.DEBIT:
                # Verificar fondos suficientes (simulado)
                pass

            # Marcar como completada
            transaction.status = TransactionStatus.COMPLETED
            transaction.updated_at = datetime.now(timezone.utc)

        except Exception as e:
            logger.warning(f"Error en lógica de negocio: {e}")
            transaction.status = TransactionStatus.FAILED
            transaction.description = str(e)

        return transaction

    async def _emit_event(self, event: DomainEvent) -> None:
        """
        Emite un evento al broker configurado.
        """
        try:
            await self._event_publisher.publish(event)
            logger.debug(f"Evento emitido: {event.event_type}")
        except Exception as e:
            # No fallar la transacción por error de emisión de evento
            logger.error(f"Error emitiendo evento {event.event_type}: {e}")

    async def _find_by_idempotency_key(
        self, idempotency_key: str
    ) -> Optional[Transaction]:
        """
        Busca una transacción por su clave de idempotencia.
        """
        # Consultar todas las transacciones del account y filtrar por idempotency_key
        # En implementación real, el repositorio tendría un método específico
        all_transactions = await self._repository.find_by_status(
            TransactionStatus.COMPLETED.value
        )
        for txn in all_transactions:
            if txn.idempotency_key == idempotency_key:
                return txn
        return None

    async def retry_failed_transaction(self, transaction_id: UUID) -> Transaction:
        """
        Reintenta una transacción que previamente falló.

        Args:
            transaction_id: ID de la transacción a reintentar

        Returns:
            Transaction: La transacción reintentada
        """
        transaction = await self._repository.find_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transacción {transaction_id} no encontrada")

        if transaction.status != TransactionStatus.FAILED:
            raise ValueError(
                f"Solo se pueden reintentar transacciones fallidas. Estado actual: {transaction.status}"
            )

        # Resetear estado y reintentar
        transaction.status = TransactionStatus.PENDING
        transaction.updated_at = datetime.now(timezone.utc)
        await self._repository.update_status(
            transaction.id, TransactionStatus.PENDING.value
        )

        return await self.execute(
            account_id=transaction.account_id,
            amount=transaction.amount,
            transaction_type=transaction.type,
            description=f"Retry: {transaction.description}",
            idempotency_key=f"retry_{transaction.idempotency_key}",
        )

    async def get_transaction_status(self, transaction_id: UUID) -> Optional[str]:
        """
        Obtiene el estado actual de una transacción.

        Args:
            transaction_id: ID de la transacción

        Returns:
            Estado de la transacción o None si no existe
        """
        transaction = await self._repository.find_by_id(transaction_id)
        return transaction.status.value if transaction else None

    async def get_account_transactions(
        self, account_id: UUID, limit: int = 100
    ) -> list[Transaction]:
        """
        Obtiene el historial de transacciones de una cuenta.

        Args:
            account_id: ID de la cuenta
            limit: Límite de resultados

        Returns:
            Lista de transacciones
        """
        return await self._repository.find_by_account_id(account_id)


class TransactionValidationError(Exception):
    """Error de validación de transacción."""
    pass


class TransactionProcessingError(Exception):
    """Error genérico de procesamiento de transacción."""
    pass