"""Entry point de la aplicación FastAPI para el sistema de procesamiento de transacciones."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.config.settings import Settings
from app.infrastructure.adapters.kafka_consumer import KafkaConsumer
from app.infrastructure.adapters.rabbitmq_consumer import RabbitMQConsumer
from app.application.handlers.transaction_event_handler import TransactionEventHandler
from app.domain.ports.event_consumer import EventConsumer
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación FastAPI."""
    settings = Settings()

    # Inicializar consumidores de eventos
    kafka_consumer: EventConsumer = KafkaConsumer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        topic=settings.kafka_transaction_topic,
        event_handler=TransactionEventHandler()
    )

    rabbitmq_consumer: EventConsumer = RabbitMQConsumer(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        queue=settings.rabbitmq_queue,
        event_handler=TransactionEventHandler()
    )

    # Iniciar consumidores en segundo plano
    await kafka_consumer.start()
    await rabbitmq_consumer.start()

    logger.info("Consumidores de eventos iniciados")
    yield

    # Cerrar consumidores al finalizar
    await kafka_consumer.stop()
    await rabbitmq_consumer.stop()
    logger.info("Consumidores de eventos detenidos")

app = FastAPI(
    title="Transaction Processing System",
    description="Sistema de procesamiento de transacciones financieras en tiempo real",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar routers (se añadirán en otros lotes)
# from app.infrastructure.api import transaction_router
# app.include_router(transaction_router.router)

@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)