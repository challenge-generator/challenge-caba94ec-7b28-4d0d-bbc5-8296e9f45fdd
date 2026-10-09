import json
import logging
from typing import Any, Dict, Optional, Type
from datetime import datetime
from pydantic import BaseModel, ValidationError

from app.domain.events import (
    DomainEvent,
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.domain.entities.transaction import Transaction

logger = logging.getLogger(__name__)


class EventSerializer:
    """Serializador/deserializador de eventos para Kafka y RabbitMQ.
    
    Utiliza Pydantic v2 para validación de esquemas.
    """

    _EVENT_TYPE_MAP: Dict[str, Type[DomainEvent]] = {
        EventType.TRANSACTION_INITIATED.value: TransactionInitiated,
        EventType.TRANSACTION_COMPLETED.value: TransactionCompleted,
        EventType.TRANSACTION_FAILED.value: TransactionFailed,
    }

    _REVERSE_EVENT_MAP: Dict[Type[DomainEvent], str] = {
        TransactionInitiated: EventType.TRANSACTION_INITIATED.value,
        TransactionCompleted: EventType.TRANSACTION_COMPLETED.value,
        TransactionFailed: EventType.TRANSACTION_FAILED.value,
    }

    def serialize(self, event: DomainEvent) -> bytes:
        """Serializa un evento a bytes para envío por middleware."""
        event_dict = self._event_to_dict(event)
        json_str = json.dumps(event_dict, default=str)
        return json_str.encode("utf-8")

    def serialize_to_dict(self, event: DomainEvent) -> Dict[str, Any]:
        """Serializa un evento a diccionario para Kafka."""
        return self._event_to_dict(event)

    def _event_to_dict(self, event: DomainEvent) -> Dict[str, Any]:
        """Convierte evento a diccionario con metadatos."""
        event_type = self._REVERSE_EVENT_MAP.get(type(event), event.event_type)
        
        event_dict = {
            "event_id": str(event.event_id),
            "event_type": event_type,
            "occurred_at": event.occurred_at.isoformat(),
            "aggregate_id": str(event.aggregate_id),
            "aggregate_type": event.aggregate_type,
            "version": event.version,
        }
        
        if isinstance(event, TransactionEvent):
            payload = event.payload
            if isinstance(payload, dict):
                event_dict.update(payload)
            else:
                event_dict["payload"] = payload.model_dump() if hasattr(payload, "model_dump") else payload.__dict__
        
        if isinstance(event, TransactionInitiated):
            event_dict.update({
                "transaction_id": str(event.transaction_id),
                "account_id": str(event.account_id),
                "amount": float(event.amount),
                "transaction_type": event.transaction_type,
            })
        elif isinstance(event, TransactionCompleted):
            event_dict.update({
                "transaction_id": str(event.transaction_id),
                "account_id": str(event.account_id),
                "amount": float(event.amount),
                "completed_at": event.completed_at.isoformat(),
            })
        elif isinstance(event, TransactionFailed):
            event_dict.update({
                "transaction_id": str(event.transaction_id),
                "account_id": str(event.account_id),
                "amount": float(event.amount),
                "failure_reason": event.failure_reason,
                "failed_at": event.failed_at.isoformat(),
            })
        
        return event_dict

    def deserialize(self, data: Dict[str, Any], event_type: Optional[str] = None) -> DomainEvent:
        """Deserializa un evento desde diccionario."""
        if event_type is None:
            event_type = data.get("event_type")
        
        if not event_type:
            raise ValueError("event_type es requerido para deserializar")
        
        event_class = self._EVENT_TYPE_MAP.get(event_type)
        if not event_class:
            raise ValueError(f"Tipo de evento desconocido: {event_type}")
        
        return self._build_event(event_class, data)

    def deserialize_from_bytes(self, data: bytes) -> DomainEvent:
        """Deserializa un evento desde bytes."""
        try:
            json_dict = json.loads(data.decode("utf-8"))
            event_type = json_dict.get("event_type")
            return self.deserialize(json_dict, event_type)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar JSON: {e}")

    def _build_event(
        self,
        event_class: Type[DomainEvent],
        data: Dict[str, Any],
    ) -> DomainEvent:
        """Construye el evento específico según su tipo."""
        base_kwargs = {
            "event_id": data.get("event_id"),
            "aggregate_id": data.get("aggregate_id"),
            "aggregate_type": data.get("aggregate_type", "Transaction"),
            "version": data.get("version", 1),
        }
        
        if "occurred_at" in data:
            base_kwargs["occurred_at"] = data["occurred_at"]
        
        if event_class == TransactionInitiated:
            return TransactionInitiated(
                **base_kwargs,
                transaction_id=data.get("transaction_id"),
                account_id=data.get("account_id"),
                amount=data.get("amount"),
                transaction_type=data.get("transaction_type"),
            )
        elif event_class == TransactionCompleted:
            completed_at = data.get("completed_at")
            return TransactionCompleted(
                **base_kwargs,
                transaction_id=data.get("transaction_id"),
                account_id=data.get("account_id"),
                amount=data.get("amount"),
                completed_at=completed_at,
            )
        elif event_class == TransactionFailed:
            failed_at = data.get("failed_at")
            return TransactionFailed(
                **base_kwargs,
                transaction_id=data.get("transaction_id"),
                account_id=data.get("account_id"),
                amount=data.get("amount"),
                failure_reason=data.get("failure_reason"),
                failed_at=failed_at,
            )
        
        raise ValueError(f"Tipo de evento no soportado: {event_class}")

    def serialize_transaction_event(
        self,
        transaction: Transaction,
        event_type: EventType,
    ) -> bytes:
        """Helper para serializar una transacción como evento."""
        event = TransactionEvent.from_transaction(transaction, event_type)
        return self.serialize(event)