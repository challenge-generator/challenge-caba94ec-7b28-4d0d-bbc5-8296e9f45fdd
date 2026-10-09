"""Configuración centralizada de la aplicación."""
from pydantic import BaseSettings, Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    """Clase de configuración utilizando Pydantic para validación."""

    # Configuración de la base de datos
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/transactions",
        env="DATABASE_URL"
    )

    # Configuración de Kafka
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        env="KAFKA_BOOTSTRAP_SERVERS"
    )
    kafka_group_id: str = Field(
        default="transaction-processing-group",
        env="KAFKA_GROUP_ID"
    )
    kafka_transaction_topic: str = Field(
        default="transactions",
        env="KAFKA_TRANSACTION_TOPIC"
    )
    kafka_error_topic: str = Field(
        default="transaction-errors",
        env="KAFKA_ERROR_TOPIC"
    )

    # Configuración de RabbitMQ
    rabbitmq_host: str = Field(
        default="localhost",
        env="RABBITMQ_HOST"
    )
    rabbitmq_port: int = Field(
        default=5672,
        env="RABBITMQ_PORT"
    )
    rabbitmq_queue: str = Field(
        default="transactions",
        env="RABBITMQ_QUEUE"
    )
    rabbitmq_error_queue: str = Field(
        default="transaction-errors",
        env="RABBITMQ_ERROR_QUEUE"
    )

    # Configuración de AWS
    aws_region: str = Field(
        default="us-east-1",
        env="AWS_REGION"
    )
    aws_access_key_id: Optional[str] = Field(
        default=None,
        env="AWS_ACCESS_KEY_ID"
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None,
        env="AWS_SECRET_ACCESS_KEY"
    )
    aws_sqs_transaction_queue_url: Optional[str] = Field(
        default=None,
        env="AWS_SQS_TRANSACTION_QUEUE_URL"
    )
    aws_sqs_error_queue_url: Optional[str] = Field(
        default=None,
        env="AWS_SQS_ERROR_QUEUE_URL"
    )

    # Configuración de la aplicación
    max_retry_attempts: int = Field(
        default=3,
        env="MAX_RETRY_ATTEMPTS"
    )
    retry_delay_seconds: int = Field(
        default=1,
        env="RETRY_DELAY_SECONDS"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False