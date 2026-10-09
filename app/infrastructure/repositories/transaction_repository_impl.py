import logging
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, update, delete, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.ports.transaction_repository import TransactionRepository
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class TransactionRepositoryImpl(TransactionRepository):
    """Implementación del repositorio de transacciones usando SQLAlchemy async.
    
    Persiste en PostgreSQL con soporte para operaciones asíncronas.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    @classmethod
    async def create(cls, settings: Settings) -> "TransactionRepositoryImpl":
        """Factory method para crear el repositorio con su conexión."""
        database_url = cls._build_database_url(settings)
        
        engine = create_async_engine(
            database_url,
            echo=settings.database_echo,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        
        async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        async with async_session_factory() as session:
            await cls._initialize_schema(session)
            return cls(session)

    @staticmethod
    def _build_database_url(settings: Settings) -> str:
        """Construye la URL de conexión a PostgreSQL."""
        return (
            f"postgresql+asyncpg://{settings.database_user}:{settings.database_password}"
            f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
        )

    @staticmethod
    async def _initialize_schema(session: AsyncSession) -> None:
        """Inicializa el schema de la base de datos si no existe."""
        from sqlalchemy import text
        try:
            await session.execute(text("SELECT 1"))
            logger.info("Conexión a PostgreSQL verificada")
        except Exception as e:
            logger.error(f"Error al verificar conexión: {e}")
            raise

    async def save(self, transaction: Transaction) -> None:
        """Guarda una nueva transacción o actualiza si ya existe."""
        try:
            stmt = insert(self._get_table()).values(
                id=str(transaction.id),
                account_id=str(transaction.account_id),
                amount=float(transaction.amount),
                type=transaction.type.value,
                status=transaction.status.value,
                idempotency_key=transaction.idempotency_key,
                description=transaction.description,
                reference=transaction.reference,
                created_at=transaction.created_at,
                updated_at=transaction.updated_at,
                completed_at=transaction.completed_at,
                failure_reason=transaction.failure_reason,
            ).on_conflict_do_nothing(
                index_elements=["idempotency_key"],
                set_={
                    "status": transaction.status.value,
                    "updated_at": datetime.utcnow(),
                }
            )
            
            await self._session.execute(stmt)
            await self._session.commit()
            logger.info(f"Transacción guardada: {transaction.id}")
            
        except IntegrityError as e:
            await self._session.rollback()
            logger.warning(f"Transacción duplicada (idempotency): {transaction.idempotency_key}")
            raise
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error(f"Error al guardar transacción: {e}")
            raise

    async def find_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        """Busca una transacción por su ID."""
        try:
            stmt = select(self._get_table()).where(
                self._get_table().c.id == str(transaction_id)
            )
            
            result = await self._session.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return self._row_to_transaction(row)
            
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar transacción por ID: {e}")
            raise

    async def find_by_account_id(self, account_id: UUID) -> List[Transaction]:
        """Busca todas las transacciones de una cuenta."""
        try:
            stmt = select(self._get_table()).where(
                self._get_table().c.account_id == str(account_id)
            ).order_by(
                self._get_table().c.created_at.desc()
            )
            
            result = await self._session.execute(stmt)
            rows = result.fetchall()
            
            return [self._row_to_transaction(row) for row in rows]
            
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar transacciones por cuenta: {e}")
            raise

    async def find_by_status(self, status: str) -> List[Transaction]:
        """Busca transacciones por estado."""
        try:
            stmt = select(self._get_table()).where(
                self._get_table().c.status == status
            ).order_by(
                self._get_table().c.created_at.desc()
            )
            
            result = await self._session.execute(stmt)
            rows = result.fetchall()
            
            return [self._row_to_transaction(row) for row in rows]
            
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar transacciones por estado: {e}")
            raise

    async def update_status(
        self,
        transaction_id: UUID,
        new_status: str,
    ) -> Optional[Transaction]:
        """Actualiza el estado de una transacción."""
        try:
            stmt = (
                update(self._get_table())
                .where(self._get_table().c.id == str(transaction_id))
                .values(
                    status=new_status,
                    updated_at=datetime.utcnow(),
                    completed_at=datetime.utcnow() if new_status == TransactionStatus.COMPLETED.value else None,
                )
                .returning(self._get_table())
            )
            
            result = await self._session.execute(stmt)
            await self._session.commit()
            
            row = result.fetchone()
            if row is None:
                return None
            
            return self._row_to_transaction(row)
            
        except SQLAlchemyError as e:
            await self._session.rollback()
            logger.error(f"Error al actualizar estado de transacción: {e}")
            raise

    def _get_table(self):
        """Retorna la tabla de transacciones para consultas."""
        from sqlalchemy import Table, Column, String, Float, DateTime, Text
        
        return Table(
            "transactions",
            Column("id", String(36), primary_key=True),
            Column("account_id", String(36), nullable=False, index=True),
            Column("amount", Float, nullable=False),
            Column("type", String(20), nullable=False),
            Column("status", String(20), nullable=False, index=True),
            Column("idempotency_key", String(100), unique=True, index=True),
            Column("description", Text),
            Column("reference", String(100)),
            Column("created_at", DateTime, nullable=False),
            Column("updated_at", DateTime, nullable=False),
            Column("completed_at", DateTime),
            Column("failure_reason", Text),
        )

    def _row_to_transaction(self, row) -> Transaction:
        """Convierte una fila de la base de datos a entidad Transaction."""
        return Transaction(
            id=UUID(row.id),
            account_id=UUID(row.account_id),
            amount=row.amount,
            type=TransactionType(row.type),
            status=TransactionStatus(row.status),
            idempotency_key=row.idempotency_key,
            description=row.description,
            reference=row.reference,
            created_at=row.created_at,
            updated_at=row.updated_at,
            completed_at=row.completed_at,
            failure_reason=row.failure_reason,
        )