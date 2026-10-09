import pytest
from unittest.mock import AsyncMock, MagicMock, call
from uuid import uuid4
from decimal import Decimal
from datetime import datetime

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.events import TransactionInitiated, TransactionCompleted, TransactionFailed
from app.domain.ports.transaction_repository import TransactionRepository


class TestProcessTransactionUseCase:
    """Tests unitarios para el caso de uso de procesamiento de transacciones."""

    @pytest.fixture
    def mock_repository(self):
        """Mock del repositorio de transacciones."""
        return AsyncMock(spec=TransactionRepository)

    @pytest.fixture
    def mock_event_publisher(self):
        """Mock del publicador de eventos."""
        return AsyncMock()

    @pytest.fixture
    def use_case(self, mock_repository, mock_event_publisher):
        """Instancia del caso de uso con dependencias inyectadas."""
        from app.application.usecases.process_transaction import ProcessTransactionUseCase
        return ProcessTransactionUseCase(mock_repository, mock_event_publisher)

    @pytest.mark.asyncio
    async def test_process_transaction_success(self, use_case, mock_repository, mock_event_publisher):
        """Verifica el flujo exitoso de procesamiento de una transacción."""
        transaction_id = uuid4()
        account_id = uuid4()

        transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("100.00"),
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

        mock_repository.save = AsyncMock(return_value=transaction)
        mock_repository.update_status = AsyncMock(return_value=transaction)

        result = await use_case.execute(transaction)

        assert result.status == TransactionStatus.COMPLETED
        mock_repository.save.assert_called_once_with(transaction)
        mock_repository.update_status.assert_called_once_with(
            transaction_id, TransactionStatus.COMPLETED.value
        )
        assert mock_event_publisher.publish.call_count == 2

    @pytest.mark.asyncio
    async def test_process_transaction_failure_invalid_amount(self, use_case, mock_repository, mock_event_publisher):
        """Verifica el manejo de transacciones con monto inválido."""
        transaction_id = uuid4()
        account_id = uuid4()

        transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("-50.00"),
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

        failed_transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("-50.00"),
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.FAILED,
            failure_reason="Monto inválido",
            created_at=datetime.now()
        )

        mock_repository.save = AsyncMock(return_value=transaction)
        mock_repository.update_status = AsyncMock(return_value=failed_transaction)

        with pytest.raises(ValueError, match="Monto inválido"):
            await use_case.execute(transaction)

    @pytest.mark.asyncio
    async def test_process_transaction_idempotency(self, use_case, mock_repository, mock_event_publisher):
        """Verifica la idempotencia del procesamiento de transacciones."""
        transaction_id = uuid4()
        account_id = uuid4()
        idempotent_key = f"{account_id}:DEPOSIT:100.00"

        transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("100.00"),
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

        mock_repository.find_by_id = AsyncMock(return_value=None)
        mock_repository.save = AsyncMock(return_value=transaction)
        mock_repository.update_status = AsyncMock(return_value=transaction)

        result = await use_case.execute(transaction)

        mock_repository.find_by_id.assert_called_once_with(transaction_id)
        mock_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_transaction_event_publishing(self, use_case, mock_repository, mock_event_publisher):
        """Verifica que los eventos se publiquen correctamente."""
        transaction_id = uuid4()
        account_id = uuid4()

        transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("250.00"),
            type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

        mock_repository.save = AsyncMock(return_value=transaction)
        mock_repository.update_status = AsyncMock(return_value=transaction)

        await use_case.execute(transaction)

        calls = mock_event_publisher.publish.call_args_list
        assert len(calls) == 2

        first_call_args = calls[0][1]
        assert first_call_args['topic'] == 'transaction.initiated'
        assert isinstance(first_call_args['event'], TransactionInitiated)

        second_call_args = calls[1][1]
        assert second_call_args['topic'] == 'transaction.completed'
        assert isinstance(second_call_args['event'], TransactionCompleted)

    @pytest.mark.asyncio
    async def test_process_transaction_repository_error(self, use_case, mock_repository, mock_event_publisher):
        """Verifica el manejo de errores del repositorio."""
        transaction_id = uuid4()
        account_id = uuid4()

        transaction = Transaction(
            id=transaction_id,
            account_id=account_id,
            amount=Decimal("100.00"),
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

        mock_repository.save = AsyncMock(side_effect=Exception("Error de base de datos"))

        with pytest.raises(Exception, match="Error de base de datos"):
            await use_case.execute(transaction)

        mock_event_publisher.publish.assert_not_called()