from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class TransactionStatus(str, Enum):
    INITIATED = "INITIATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"

class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    account_id: UUID
    amount: float = Field(gt=0, description="Transaction amount must be positive")
    currency: str = Field(min_length=3, max_length=3, description="Currency code in ISO 4217 format")
    type: TransactionType
    status: TransactionStatus = TransactionStatus.INITIATED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = Field(default=None, description="Additional transaction metadata")

    def complete(self) -> None:
        if self.status != TransactionStatus.INITIATED:
            raise ValueError(f"Cannot complete transaction with status {self.status}")
        self.status = TransactionStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def fail(self, reason: str) -> None:
        if self.status != TransactionStatus.INITIATED:
            raise ValueError(f"Cannot fail transaction with status {self.status}")
        self.status = TransactionStatus.FAILED
        self.updated_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}
        self.metadata["failure_reason"] = reason

    def is_idempotent_key(self) -> str:
        return f"{self.account_id}_{self.amount}_{self.currency}_{self.type.value}"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
        from_attributes = True
        frozen = False