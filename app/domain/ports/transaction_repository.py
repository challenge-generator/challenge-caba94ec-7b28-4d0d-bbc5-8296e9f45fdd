from typing import Protocol, Optional, List
from uuid import UUID
from app.domain.entities.transaction import Transaction

class TransactionRepository(Protocol):
    async def save(self, transaction: Transaction) -> None:
        """Persists a transaction in the repository."""
        ...

    async def find_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """Finds a transaction by its ID."""
        ...

    async def find_by_account_id(self, account_id: UUID) -> List[Transaction]:
        """Finds all transactions for a given account ID."""
        ...

    async def find_by_status(self, status: str) -> List[Transaction]:
        """Finds all transactions with the given status."""
        ...

    async def update_status(self, transaction_id: UUID, new_status: str) -> Optional[Transaction]:
        """Updates the status of a transaction and returns the updated transaction."""
        ...