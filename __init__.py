"""
Paquete principal de la aplicación de procesamiento de transacciones financieras.
Contiene la estructura hexagonal con dominio, aplicación e infraestructura.
"""

from app.domain.entities.transaction import (
    Transaction,
    TransactionStatus,
    TransactionType,
)
from app.domain.events import (
    DomainEvent,
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
)
from app.domain.ports.transaction_repository import TransactionRepository

__version__ = "0.1.0"
__author__ = "Pragma Engineering"
__license__ = "MIT"

__all__ = [
    "Transaction",
    "TransactionStatus",
    "TransactionType",
    "DomainEvent",
    "TransactionEvent",
    "TransactionInitiated",
    "TransactionCompleted",
    "TransactionFailed",
    "TransactionRepository",
]


def get_app_info() -> dict:
    """Retorna información básica de la aplicación."""
    return {
        "name": "transaction-processing-system",
        "version": __version__,
        "description": "Sistema EDA para procesamiento de transacciones financieras en tiempo real",
        "architecture": "hexagonal/clean con enfoque reactivo",
    }