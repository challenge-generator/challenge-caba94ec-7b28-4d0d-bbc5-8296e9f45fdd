from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from uuid import UUID
from app.domain.entities.transaction import Transaction, TransactionStatus

EventType = Literal["TransactionInitiated", "TransactionCompleted", "TransactionFailed"]

class DomainEvent(BaseModel):
    event_id: UUID
    event_type: EventType
    timestamp: datetime
    payload: dict
    metadata: dict = {}

    def __init__(self, **data):
        super().__init__(**data)
        if not self.metadata:
            self.metadata = {}

class TransactionEvent(DomainEvent):
    transaction_id: UUID
    account_id: UUID
    amount: float
    currency: str
    status: TransactionStatus
    transaction_type: str

    @classmethod
    def from_transaction(cls, transaction: Transaction, event_type: EventType) -> 'TransactionEvent':
        return cls(
            event_id=transaction.id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            transaction_id=transaction.id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            currency=transaction.currency,
            status=transaction.status,
            transaction_type=transaction.type.value,
            payload={
                "transaction_id": str(transaction.id),
                "account_id": str(transaction.account_id),
                "amount": transaction.amount,
                "currency": transaction.currency,
                "type": transaction.type.value,
                "status": transaction.status.value
            }
        )

class TransactionInitiated(TransactionEvent):
    pass

class TransactionCompleted(TransactionEvent):
    pass

class TransactionFailed(TransactionEvent):
    failure_reason: str

    def __init__(self, **data):
        super().__init__(**data)
        if "failure_reason" not in self.payload:
            self.payload["failure_reason"] = data.get("failure_reason", "Unknown error")