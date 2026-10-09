# Prompt para Mejorar el Codigo Base

Copia y pega el contenido del bloque de abajo en un asistente de IA (Claude, ChatGPT)
para obtener un ZIP con el proyecto completo y arrancable.

Si preferis trabajar en tu editor con un agente local (Claude Code, Cursor, Copilot), usa `AGENTS.md` en vez de este archivo: dice lo mismo pero para que escriba los archivos en disco.

## Las dos reglas que no se negocian

1. **Completa el boilerplate.** Todo lo que el proyecto necesita para compilar y arrancar: manifiesto de dependencias, punto de entrada, configuracion, capa de interfaz, y las capas del patron arquitectonico declarado. Eso es andamiaje y es tu trabajo.
2. **NO resuelvas el reto.** Los entregables de las fases son el trabajo de la persona. El hueco pedagogico se deja como esta: el proyecto arranca, pero lo que el reto pide implementar NO esta implementado.

Dicho de otra forma: si algo impide compilar, arreglalo. Si algo es logica de negocio incompleta, validaciones ausentes, un secreto hardcodeado o un patron mejorable, dejalo exactamente como esta — es lo que la persona tiene que encontrar.

## Lo que le falta a este proyecto

Esto NO lo tenes que adivinar: salio de comparar el proyecto contra la arquitectura declarada del reto y de un analisis estatico del codigo. Completalo TODO.

### Boilerplate del stack que falta

Sin esto no compila ni arranca. Es andamiaje, no toca nada de lo pedagogico:

- **__init__.py** — Sin __init__.py, app no es un paquete importable y "import app.main" falla.

### Archivos que la arquitectura del reto declara y no estan

Creálos con implementacion real, en la capa que les corresponde:

- `README.md`

### Referencias colgando en el codigo que si esta

Cada una rompe la compilacion:

- `app/main.py` — `EventConsumer.start`: Se invoca `start` sobre `EventConsumer`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/main.py` — `EventConsumer.stop`: Se invoca `stop` sobre `EventConsumer`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/usecases/process_transaction.py` — `TransactionRepository.info`: Se invoca `info` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/usecases/process_transaction.py` — `TransactionRepository.error`: Se invoca `error` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/usecases/process_transaction.py` — `TransactionRepository.warning`: Se invoca `warning` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/usecases/process_transaction.py` — `TransactionRepository.debug`: Se invoca `debug` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.info`: Se invoca `info` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.warning`: Se invoca `warning` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.debug`: Se invoca `debug` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.error`: Se invoca `error` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.info`: Se invoca `info` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.error`: Se invoca `error` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.warning`: Se invoca `warning` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

## Como saber que terminaste

```bash
pip install -r requirements.txt && python -c "import app.main"
```

Ese comando corriendo sin errores es la definicion de "listo".

---

```
## Briefing del reto (autoridad)
Este bloque manda sobre los archivos adjuntos. El stack y el rol salen de AQUÍ, no de un topic genérico ni de markdown placeholder.

### Perfil
Chapter Backend, Especialidad Desarrollador, Tecnología Python, Senior

### Brecha de conocimiento
Implementa soluciones basada en arquitectura orientada a eventos (EDA) y tiene un sólido conocimiento de los conceptos relacionados con este tipo de arquitectura para implementar y mantener sistemas eficientes y escalables. Experiencia comprobable en al menos una herramienta como Apache Kafka, RabbitMQ, SQS, EventBridge, etc.

### Misión / candidato
Candidato Senior con experiencia en backend.

### Reto
- Tema: Implementa y Mantiene de Sistemas EDA con Dominio de Kafka, RabbitMQ y más
- Seniority: senior-l2
- Tipo: practical
- Título: Diseño y Mantenimiento de Sistema EDA en Banca
- Tiempo estimado: 15 horas

### Fases (trabajo del HUMANO — PROHIBIDO completarlas)
No implementes estos entregables. Dejalos como hueco pedagógico. El asistente solo materializa el proyecto arrancable para que el participante pueda trabajar.
- Fase 1: Definición del Dominio y Requisitos — objetivo: Establecer los requisitos del sistema y definir el dominio de las transacciones financieras. — entregable (NO resolver): Documento de requisitos del sistema con eventos definidos, umbrales y restricciones.
- Fase 2: Diseño del Sistema EDA — objetivo: Diseñar la arquitectura del sistema EDA integrando Apache Kafka y RabbitMQ. — entregable (NO resolver): Documento de diseño del sistema EDA con decisiones de integración y trade-offs documentados.
- Fase 3: Implementación y Validación — objetivo: Implementar el sistema EDA y validar su funcionamiento. — entregable (NO resolver): Sistema EDA implementado y documentado con resultados de pruebas y ajustes.
- Fase 4: Mantenimiento y Optimización — objetivo: Mantener y optimizar el sistema EDA para asegurar su eficiencia y escalabilidad a largo plazo. — entregable (NO resolver): Sistema EDA optimizado y documentado con cambios realizados y resultados de pruebas de regresión.

Eres un asistente experto en análisis, corrección y generación de archivos de cualquier tipo:
código fuente, documentación, hojas de cálculo, documentos Word, configuraciones, entre otros.
Voy a enviarte una cadena de texto que contiene uno o más archivos. Cada archivo está delimitado por un marcador con el siguiente formato:
// === ARCHIVO: ruta/del/archivo.extension ===
o también puede aparecer como:
## === ARCHIVO: ruta/del/archivo.extension ===
Lo que sigue al marcador puede ser:

El contenido real del archivo (código, texto, YAML, etc.)
Una descripción en lenguaje natural de lo que debe contener el archivo


TU TAREA
PASO 0 — ¿Esto es un proyecto o una carcasa?
Antes de extraer archivos, leé el Briefing (si está) y diagnosticá el adjunto.

Es CARCASA si ocurre CUALQUIERA de estas:
- No hay manifiesto de dependencias del stack del briefing (manifest.json de VTEX IO / package.json / pom.xml / build.gradle / requirements.txt / go.mod / *.tf / *.csproj, según corresponda)
- Hay un "binario" que en realidad es un comentario ("no puede ser mostrado como texto plano", placeholder .fig/.docx vacío)
- Los markdowns ya completan entregables de fases posteriores ("se implementó fade-in", lista de áreas ya resuelta)

Si es CARCASA:
- MATERIALIZÁ un proyecto que arranca en el stack del briefing (VTEX IO Store Framework, Angular, Terraform, pytest, Nest, etc.). Incluí manifiesto, punto de entrada y capa de interfaz reales.
- NO copies los markdowns de "solución" como si fueran el producto. Son ruido de generación.
- NO resuelvas las fases del briefing (están marcadas PROHIBIDO). Dejá el hueco pedagógico: el flujo existe, las microinteracciones/calidad/infra que el reto pide NO están hechas.
- Después seguí al PASO 5 (ZIP).

Si es un proyecto REAL (manifiesto + código que compila o arranca):
- Seguí PASO 1 en adelante. 🔴 compilación sí. 🟡 pedagógico no.

PASO 1 — Detección y extracción
Identifica todos los archivos presentes en la cadena. Para cada archivo extrae:

Su ruta completa (ej: src/main/java/com/pragma/Service.java)
Su contenido o descripción

PASO 2 — Clasificación por tipo
Clasifica cada archivo en una de estas categorías:
A) Código fuente (Java, Python, TypeScript, JavaScript, Kotlin, etc.)
B) Configuración / documentación (YAML, properties, Markdown, JSON, txt, etc.)
C) Excel (.xlsx, .xls, .csv)
D) Word (.docx, .doc)
E) Otro tipo de archivo binario o especial
PASO 3 — Clasificación de errores en código fuente

Objetivo prioritario: que el proyecto compile. No corrijas flujo de negocio ni lógica funcional.

Antes de modificar cualquier archivo de código fuente, clasifica cada problema encontrado en una de estas dos categorías:
🔴 ERROR DE COMPILACIÓN — corregir siempre
Son errores que impiden que el proyecto arranque, sin valor pedagógico:

Import faltante o incorrecto
Clase, método o variable referenciada que no existe en ningún archivo del proyecto
Error de sintaxis
Anotación con atributos inválidos
Dependencia ausente en pom.xml, package.json, etc.
Archivo referenciado que no existe y debe ser creado con implementación mínima

→ CORREGIR estos errores.
🟡 PROBLEMA FUNCIONAL O DE CALIDAD — preservar siempre
Son problemas que no impiden compilar. Pueden ser intencionales para el aprendizaje:

Clave secreta hardcodeada ("secret", "password123")
API deprecada que funciona pero tiene reemplazo moderno
Lógica de negocio incorrecta o incompleta
Código redundante o de baja legibilidad
Falta de validaciones en flujo de negocio
Patrones de diseño incorrectos pero funcionales
Concurrencia no segura
Configuración funcional pero no óptima

→ PRESERVAR tal cual. No corregir, no mejorar, no comentar.
PASO 4 — Procesamiento según tipo de archivo
Tipo A — Código fuente
Aplica únicamente las correcciones clasificadas como 🔴 ERROR DE COMPILACIÓN.
No alteres ningún elemento clasificado como 🟡 PROBLEMA FUNCIONAL O DE CALIDAD.
Si falta un archivo referenciado, créalo con la implementación mínima necesaria para compilar.
Tipo B — Configuración / documentación
Extrae el contenido tal cual, sin modificaciones salvo errores evidentes de sintaxis
(ej: YAML mal indentado).
Tipo C — Excel (.xlsx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un archivo Excel funcional con:

Fila de encabezados en negrita con color de fondo distintivo
Columnas con ancho ajustado al contenido
Tipos de dato correctos por columna
Validaciones si la descripción lo indica
Hojas nombradas descriptivamente si hay más de una
Filas de ejemplo si no hay datos reales

Tipo D — Word (.docx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un documento Word funcional con:

Estilos de título (Título 1, Título 2) para jerarquía de secciones
Fuente legible (Calibri o equivalente), tamaño 11-12pt para cuerpo
Márgenes estándar
Tabla de contenido si tiene múltiples secciones
Tablas con encabezados en negrita si aplica

Tipo E — Otro
Genera el archivo con el contenido o estructura más apropiada según la descripción.
PASO 5 — Exportación en ZIP
Empaqueta todos los archivos en un único archivo ZIP descargable respetando exactamente
la estructura de rutas indicada por los marcadores.
El ZIP debe incluir:

Archivos de código con únicamente los errores de compilación corregidos
Archivos de configuración y documentación sin cambios
Archivos nuevos creados para resolver dependencias de compilación faltantes
Archivos Excel y Word generados desde descripción

IMPORTANTE: El ZIP debe estar listo para descargar al finalizar. No preguntes si el usuario
quiere generarlo. Simplemente genera el archivo y proporciona el enlace de descarga; No debes desplegar en el chat el resumen de lo que arreglaste al Zip, solo entregalo.

REGLAS IMPORTANTES

No omitas ningún archivo aunque no tenga errores ni modificaciones
Respeta los nombres y rutas exactas indicadas por los marcadores
Si un archivo no tiene marcador claro, infiere el nombre desde su contenido
Si la cadena contiene solo documentación, placeholders o binarios fake, NO la reproduzcas:
aplicá PASO 0 (materializar el proyecto del briefing). Reproducir la carcasa es un fallo.
No agregues texto después del enlace de descarga del ZIP
No preguntes si el usuario quiere el ZIP: simplemente generalo siempre
Si detectas que falta un archivo de configuración necesario para compilar
(pom.xml, package.json, requirements.txt, build.gradle, etc.), créalo e inclúyelo
inferiendo su contenido desde los imports y frameworks detectados en el código
Nunca corrijas problemas 🟡 aunque parezcan obvios o fáciles de mejorar.
El participante que recibirá este proyecto los debe encontrar y resolver él mismo.


INPUT
Aquí está la cadena con los archivos:

// === ARCHIVO: pyproject.toml ===
[tool.poetry]
name = "transaction-processing-system"
version = "0.1.0"
description = "Sistema EDA para procesamiento de transacciones financieras en tiempo real"
authors = ["Pragma Engineering"]
license = "MIT"
readme = "README.md"
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.13"
fastapi = "0.115.0"
uvicorn = "0.30.5"
pydantic = "2.9.0"
sqlalchemy = "2.0.32"
asyncpg = "0.29.0"
confluent-kafka = "2.5.0"
pika = "1.3.2"
boto3 = "1.35.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.test.dependencies]
pytest = "8.2.2"
pytest-asyncio = "0.24.0"
httpx = "0.27.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = "test_*.py"

// === ARCHIVO: app/main.py ===
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

// === ARCHIVO: app/infrastructure/config/settings.py ===
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

// === ARCHIVO: app/domain/entities/transaction.py ===
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

// === ARCHIVO: app/domain/events/__init__.py ===
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

// === ARCHIVO: app/domain/ports/transaction_repository.py ===
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

// === ARCHIVO: app/domain/ports/event_publisher.py ===
"""
Puerto para la publicación de eventos del dominio.
Define el contrato que la infraestructura debe implementar para emitir
eventos a sistemas de mensajería como Kafka, RabbitMQ o SQS.
"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.events import TransactionEvent, TransactionInitiated, TransactionCompleted, TransactionFailed


class EventPublisher(ABC):
    """
    Interfaz abstracta para publicar eventos del dominio.
    
    La implementación concreta será inyectada por el contenedor de dependencias
    y puede variar según el entorno (desarrollo, testing, producción).
    """

    @abstractmethod
    async def publish_transaction_initiated(
        self,
        event: TransactionInitiated,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción iniciada.
        
        Args:
            event: Evento de dominio con los datos de la transacción.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish_transaction_completed(
        self,
        event: TransactionCompleted,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción completada.
        
        Args:
            event: Evento de dominio con los datos de la transacción completada.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish_transaction_failed(
        self,
        event: TransactionFailed,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento de transacción fallida.
        
        Args:
            event: Evento de dominio con los datos del fallo.
            idempotency_key: Clave para garantizar idempotencia en la publicación.
            
        Returns:
            True si el evento fue publicado exitosamente, False en caso contrario.
        """
        pass

    @abstractmethod
    async def publish(
        self,
        event: TransactionEvent,
        topic: str,
        idempotency_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento genérico al topic especificado.
        
        Args:
            event: Cualquier evento de transacción del dominio.
            topic: Nombre del topic o cola de destino.
            idempotency_key: Clave para garantizar idempotencia.
            
        Returns:
            True si el evento fue publicado exitosamente.
        """
        pass

    @abstractmethod
    async def publish_batch(
        self,
        events: list[TransactionEvent],
        topic: str,
        idempotency_key_prefix: Optional[str] = None
    ) -> list[bool]:
        """
        Publica un lote de eventos de manera eficiente.
        
        Optimizado para alto throughput (5000 TPS objetivo).
        
        Args:
            events: Lista de eventos a publicar.
            topic: Nombre del topic o cola de destino.
            idempotency_key_prefix: Prefijo para generar claves de idempotencia.
            
        Returns:
            Lista de booleanos indicando éxito o fracaso de cada publicación.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Cierra las conexiones y libera recursos del publisher.
        Debe ser llamado al shutting down de la aplicación.
        """
        pass

// === ARCHIVO: app/domain/ports/event_consumer.py ===
"""
Puerto para el consumo de eventos del dominio.
Define el contrato que la infraestructura debe implementar para suscribirse
y procesar eventos desde sistemas de mensajería como Kafka, RabbitMQ o SQS.
"""
from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Optional
from uuid import UUID

from app.domain.events import TransactionEvent, TransactionInitiated, TransactionCompleted, TransactionFailed


EventHandler = Callable[[TransactionEvent], Awaitable[None]]
"""
Tipo que define un handler de evento.
Cada handler procesa un evento de dominio específico.
"""


class MessageProcessingResult:
    """
    Resultado del procesamiento de un mensaje.
    Permite trackear el estado y metadatos del procesamiento.
    """
    
    def __init__(
        self,
        success: bool,
        event_id: Optional[UUID] = None,
        error_message: Optional[str] = None,
        retry_count: int = 0
    ):
        self.success = success
        self.event_id = event_id
        self.error_message = error_message
        self.retry_count = retry_count
        
    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"<MessageProcessingResult {status} event_id={self.event_id} retries={self.retry_count}>"


class EventConsumer(ABC):
    """
    Interfaz abstracta para consumir eventos del dominio.
    
    La implementación concreta (Kafka, RabbitMQ, SQS) será inyectada
    y procesará eventos según la configuración del sistema.
    """

    @abstractmethod
    async def subscribe_to_transaction_initiated(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción iniciada.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe_to_transaction_completed(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción completada.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe_to_transaction_failed(
        self,
        handler: EventHandler,
        topic: str
    ) -> None:
        """
        Suscribe un handler para procesar eventos de transacción fallida.
        
        Args:
            handler: Función async que procesa el evento.
            topic: Topic o cola de suscripción.
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        topic: str,
        handler: EventHandler,
        event_type_filter: Optional[type[TransactionEvent]] = None
    ) -> None:
        """
        Suscribe un handler genérico a un topic.
        
        Args:
            topic: Topic o cola a escuchar.
            handler: Función que procesa cualquier evento recibido.
            event_type_filter: Filtro opcional por tipo de evento.
        """
        pass

    @abstractmethod
    async def start_consuming(self) -> None:
        """
        Inicia el consumo de mensajes.
        Bloquea hasta que se detenga el consumidor.
        """
        pass

    @abstractmethod
    async def stop_consuming(self) -> None:
        """
        Detiene el consumo de mensajes de manera graceful.
        Procesa los mensajes en flight antes de cerrar.
        """
        pass

    @abstractmethod
    async def process_message(
        self,
        raw_message: bytes,
        handler: EventHandler
    ) -> MessageProcessingResult:
        """
        Procesa un mensaje raw deserializándolo y ejecutando el handler.
        
        Args:
            raw_message: Mensaje en bytes del broker de mensajería.
            handler: Handler a ejecutar con el evento deserializado.
            
        Returns:
            Resultado del procesamiento con éxito/fracaso y metadatos.
        """
        pass

    @abstractmethod
    def is_consuming(self) -> bool:
        """
        Verifica si el consumidor está activo.
        
        Returns:
            True si está consumiendo mensajes, False si está detenido.
        """
        pass

    @abstractmethod
    async def get_consumer_stats(self) -> dict:
        """
        Obtiene estadísticas del consumidor para monitoreo.
        
        Returns:
            Diccionario con métricas: mensajes procesados, errores, latencia, etc.
        """
        pass

// === ARCHIVO: __init__.py ===
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

// === ARCHIVO: Dockerfile ===
# Stage 1: Builder - Instala dependencias y prepara el entorno
FROM python:3.13-slim AS builder

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.4

# Instalar Poetry para gestión de dependencias
RUN pip install poetry==${POETRY_VERSION}

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo archivos necesarios para instalar dependencias
COPY pyproject.toml pyproject.lock* ./

# Configurar Poetry para instalar en el directorio del proyecto
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Stage 2: Production - Imagen final optimizada
FROM python:3.13-slim AS production

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000

# Crear usuario no-root para seguridad
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Instalar dependencias del sistema necesarias para las librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    librdkafka5 \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Copiar la aplicación del stage builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Crear directorios necesarios con permisos
RUN mkdir -p /app/logs /app/data /app/config && \
    chown -R appuser:appgroup /app

# Cambiar al usuario no-root
USER appuser

# Exponer puerto de la aplicación
EXPOSE 8000

# Etiquetas de metadata
LABEL maintainer="Pragma Engineering" \
      version="0.1.0" \
      description="Sistema EDA para procesamiento de transacciones financieras"

# Healthcheck para verificar que la aplicación está corriendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health') or exit(1)"

# Comando de inicio de la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

// === ARCHIVO: .dockerignore ===
# Archivos y directorios de Python que no deben incluirse en la imagen
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Entornos virtuales de Python
venv/
env/
ENV/
.venv

# Archivos de Poetry
poetry.lock

# Archivos de configuración de desarrollo local
.env
.env.local
.env.*.local
*.local

# Archivos de IDE y editor
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store

# Archivos de Git
.git/
.gitignore
.gitattributes

# Documentación
*.md
docs/
tutorial/

# Tests
tests/
test_*.py
*_test.py
conftest.py
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Logs
*.log
logs/

# Archivos temporales
tmp/
temp/
.cache/

# Archivos de infraestructura (se manejan externamente)
docker-compose*.yml
docker-compose*.yaml
Dockerfile.dev

# Certificados y claves (nunca incluir en imagen)
*.pem
*.key
*.crt
credentials.json
*.credentials

// === ARCHIVO: docker-compose.yml ===
version: '3.8'

services:
  postgres:
    image: postgres:16.4
    container_name: transaction-postgres
    environment:
      POSTGRES_USER: transaction_user
      POSTGRES_PASSWORD: transaction_pass
      POSTGRES_DB: transaction_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U transaction_user -d transaction_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - transaction-network

  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    container_name: transaction-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "2181"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - transaction-network

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: transaction-kafka
    depends_on:
      zookeeper:
        condition: service_healthy
    ports:
      - "9092:9092"
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_HOST://localhost:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_LOG_RETENTION_HOURS: 168
      KAFKA_LOG_SEGMENT_BYTES: 1073741824
      KAFKA_NUM_PARTITIONS: 6
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
    healthcheck:
      test: ["CMD", "kafka-broker-api-versions", "--bootstrap-server", "localhost:9092"]
      interval: 10s
      timeout: 10s
      retries: 5
    networks:
      - transaction-network

  rabbitmq:
    image: rabbitmq:3.13-management
    container_name: transaction-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: transaction_user
      RABBITMQ_DEFAULT_PASS: transaction_pass
      RABBITMQ_DEFAULT_VHOST: /
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - transaction-network

  localstack:
    image: localstack/localstack:3.0
    container_name: transaction-localstack
    environment:
      SERVICES: sqs,sns
      DEBUG: "1"
      DEFAULT_REGION: us-east-1
      DOCKER_HOST: unix:///var/run/docker.sock
      EAGER_SERVICE_LOADING: "1"
    ports:
      - "4566:4566"
    volumes:
      - localstack_data:/var/lib/localstack
      - /var/run/docker.sock:/var/run/docker.sock
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
      interval: 15s
      timeout: 10s
      retries: 5
    networks:
      - transaction-network

volumes:
  postgres_data:
    driver: local
  rabbitmq_data:
    driver: local
  localstack_data:
    driver: local

networks:
  transaction-network:
    driver: bridge

// === ARCHIVO: app/application/usecases/process_transaction.py ===
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

// === ARCHIVO: app/application/handlers/transaction_event_handler.py ===
import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.domain.entities.transaction import Transaction, TransactionStatus
from app.domain.events import (
    DomainEvent,
    TransactionCompleted,
    TransactionEvent,
    TransactionFailed,
    TransactionInitiated,
)
from app.domain.ports.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)


class TransactionEventHandler:
    """
    Manejador de eventos para procesar eventos entrantes del sistema EDA.
    Actualiza el estado de las transacciones y coordina flujos derivados.
    """

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        event_publisher,  # EventPublisher del dominio
    ):
        self._repository = transaction_repository
        self._event_publisher = event_publisher

    async def handle_transaction_initiated(
        self, event: TransactionInitiated
    ) -> None:
        """
        Procesa el evento de transacción iniciada.
        Puede iniciar verificaciones adicionales o flujos derivados.

        Args:
            event: Evento de transacción iniciada
        """
        logger.info(
            f"Manejando TransactionInitiated para {event.transaction_id}"
        )

        # Buscar la transacción
        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.warning(
                f"Transacción {event.transaction_id} no encontrada para evento"
            )
            return

        # Verificar que el estado sea consistente
        if transaction.status != TransactionStatus.PENDING:
            logger.warning(
                f"Transacción {event.transaction_id} en estado inesperado: {transaction.status}"
            )
            return

        # Aquí se pueden lanzar flujos derivados:
        # - Notificaciones al usuario
        # - Verificaciones de fraude
        # - Reservas de fondos
        # Por ahora, solo registramos el procesamiento
        logger.debug(
            f"Evento TransactionInitiated procesado para {event.transaction_id}"
        )

    async def handle_transaction_completed(
        self, event: TransactionCompleted
    ) -> None:
        """
        Procesa el evento de transacción completada.
        Actualiza el estado y puede iniciar flujos post-completación.

        Args:
            event: Evento de transacción completada
        """
        logger.info(
            f"Manejando TransactionCompleted para {event.transaction_id}"
        )

        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.error(
                f"Transacción {event.transaction_id} no encontrada para completación"
            )
            return

        # Actualizar estado en repositorio
        await self._repository.update_status(
            event.transaction_id, TransactionStatus.COMPLETED.value
        )

        # Post-procesamiento: notificaciones, sincronización, etc.
        await self._trigger_post_completion_actions(transaction)

        logger.info(
            f"Transacción {event.transaction_id} procesada completamente"
        )

    async def handle_transaction_failed(
        self, event: TransactionFailed
    ) -> None:
        """
        Procesa el evento de transacción fallida.
        Registra la falla y puede iniciar flujos de compensación.

        Args:
            event: Evento de transacción fallida
        """
        logger.warning(
            f"Manejando TransactionFailed para {event.transaction_id}: {event.failure_reason}"
        )

        transaction = await self._repository.find_by_id(event.transaction_id)
        if not transaction:
            logger.error(
                f"Transacción {event.transaction_id} no encontrada para manejo de falla"
            )
            return

        # Actualizar estado a fallido
        await self._repository.update_status(
            event.transaction_id, TransactionStatus.FAILED.value
        )

        # Acciones de compensación: liberar fondos, notificar al usuario, etc.
        await self._trigger_compensation_actions(transaction, event.failure_reason)

        logger.info(
            f"Transacción {event.transaction_id} marcada como fallida"
        )

    async def handle_event(self, event: DomainEvent) -> None:
        """
        Dispatcher principal que redirige al handler apropiado según el tipo de evento.

        Args:
            event: Evento de dominio a procesar
        """
        if isinstance(event, TransactionInitiated):
            await self.handle_transaction_initiated(event)
        elif isinstance(event, TransactionCompleted):
            await self.handle_transaction_completed(event)
        elif isinstance(event, TransactionFailed):
            await self.handle_transaction_failed(event)
        else:
            logger.warning(f"Tipo de evento no manejado: {type(event)}")

    async def _trigger_post_completion_actions(
        self, transaction: Transaction
    ) -> None:
        """
        Ejecuta acciones derivadas después de una transacción completada.
        Ejemplo: notificaciones, actualización de balances, etc.
        """
        # Simular acciones post-completación
        logger.debug(
            f"Ejecutando acciones post-completación para {transaction.id}"
        )

        # En implementación real:
        # - Notificar al usuario via email/push
        # - Actualizar balance de cuenta
        # - Generar comprobante
        # - Integrar con sistema contable

    async def _trigger_compensation_actions(
        self, transaction: Transaction, failure_reason: str
    ) -> None:
        """
        Ejecuta acciones de compensación cuando una transacción falla.

        Args:
            transaction: Transacción que falló
            failure_reason: Razón de la falla
        """
        logger.debug(
            f"Ejecutando acciones de compensación para {transaction.id}"
        )

        # En implementación real:
        # - Liberar fondos reservados
        # - Notificar al usuario del fracaso
        # - Registrar en log de auditoría
        # - Integrar con sistema de alertas

    async def get_pending_transactions(self) -> list[Transaction]:
        """
        Recupera todas las transacciones pendientes para monitoreo.

        Returns:
            Lista de transacciones en estado PENDING
        """
        return await self._repository.find_by_status(TransactionStatus.PENDING.value)

    async def recover_stale_transactions(self, max_age_minutes: int = 30) -> int:
        """
        Recupera transacciones que quedaron en estado PENDING por mucho tiempo.

        Args:
            max_age_minutes: Antigüedad máxima en minutos

        Returns:
            Cantidad de transacciones recuperadas
        """
        pending = await self.get_pending_transactions()
        recovered_count = 0

        now = datetime.now(timezone.utc)
        for txn in pending:
            age = (now - txn.updated_at).total_seconds() / 60
            if age > max_age_minutes:
                logger.info(
                    f"Recuperando transacción estancada {txn.id} (edad: {age:.1f} min)"
                )
                # Marcar como fallida por timeout
                await self._repository.update_status(
                    txn.id, TransactionStatus.FAILED.value
                )
                recovered_count += 1

        return recovered_count

    async def replay_event(self, event: TransactionEvent) -> bool:
        """
        Reproduce un evento para recuperación o debugging.

        Args:
            event: Evento a reproducir

        Returns:
            True si se procesó correctamente
        """
        logger.info(f"Reproduciendo evento {event.event_id}")
        try:
            await self.handle_event(event)
            return True
        except Exception as e:
            logger.error(f"Error reproduciendo evento {event.event_id}: {e}")
            return False

// === ARCHIVO: app/infrastructure/adapters/kafka_producer.py ===
import logging
import asyncio
from typing import Optional
from uuid import UUID

from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class KafkaProducerAdapter:
    """Adaptador para publicar eventos en Apache Kafka.
    
    Implementa el patrón de adaptador para el puerto EventPublisher.
    Maneja la serialización de eventos y la configuración de entrega
    con garantías de tolerancia a fallos.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._producer: Optional[Producer] = None
        self._topics = {
            EventType.TRANSACTION_INITIATED: settings.kafka_topic_transactions,
            EventType.TRANSACTION_COMPLETED: settings.kafka_topic_transactions,
            EventType.TRANSACTION_FAILED: settings.kafka_topic_transactions,
        }
        self._delivery_reports: dict = {}
        self._init_producer()
    
    def _init_producer(self) -> None:
        """Inicializa el productor de Kafka con configuración optimizada."""
        config = {
            'bootstrap.servers': self._settings.kafka_bootstrap_servers,
            'client.id': self._settings.kafka_client_id,
            'acks': self._settings.kafka_acks,
            'retries': self._settings.kafka_retries,
            'retry.backoff.ms': self._settings.kafka_retry_backoff_ms,
            'enable.idempotence': True,
            'max.in.flight.requests.per.connection': 5,
            'compression.type': 'lz4',
            'linger.ms': 5,
            'batch.size': 16384,
        }
        self._producer = Producer(config)
        logger.info(f"Productor Kafka inicializado hacia {self._settings.kafka_bootstrap_servers}")
    
    def _delivery_callback(self, err, msg) -> None:
        """Callback para reportes de entrega de mensajes."""
        if err is not None:
            logger.error(f"Error en entrega de mensaje: {err}")
            self._delivery_reports[msg.topic()] = {'success': False, 'error': str(err)}
        else:
            logger.debug(f"Mensaje entregado a {msg.topic()} [{msg.partition()}] offset {msg.offset()}")
            self._delivery_reports[msg.topic()] = {'success': True, 'offset': msg.offset()}
    
    async def publish(self, event: TransactionEvent) -> bool:
        """Publica un evento en el topic de Kafka correspondiente.
        
        Args:
            event: Evento de dominio a publicar.
            
        Returns:
            True si el evento se publicó exitosamente, False en caso contrario.
        """
        if self._producer is None:
            logger.error("Productor Kafka no inicializado")
            return False
        
        try:
            topic = self._topics.get(event.event_type)
            if not topic:
                logger.error(f"Topic no configurado para evento tipo {event.event_type}")
                return False
            
            message_key = event.transaction_id
            message_value = event.model_dump_json()
            
            self._producer.produce(
                topic=topic,
                key=message_key,
                value=message_value,
                callback=self._delivery_callback,
            )
            self._producer.poll(0)
            
            logger.info(f"Evento {event.event_type.value} publicado para transacción {message_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error publicando evento en Kafka: {e}")
            return False
    
    async def publish_batch(self, events: list[TransactionEvent]) -> int:
        """Publica un lote de eventos de forma eficiente.
        
        Args:
            events: Lista de eventos a publicar.
            
        Returns:
            Número de eventos publicados exitosamente.
        """
        success_count = 0
        for event in events:
            if await self.publish(event):
                success_count += 1
        
        self._producer.flush()
        logger.info(f"Publicados {success_count}/{len(events)} eventos del lote")
        return success_count
    
    async def create_topics(self) -> None:
        """Crea los topics de Kafka si no existen."""
        admin_client = AdminClient({
            'bootstrap.servers': self._settings.kafka_bootstrap_servers
        })
        
        topics_to_create = [
            NewTopic(
                self._settings.kafka_topic_transactions,
                num_partitions=self._settings.kafka_num_partitions,
                replication_factor=self._settings.kafka_replication_factor,
            ),
        ]
        
        try:
            fs = admin_client.create_topics(topics_to_create, validate_only=True)
            for topic, f in fs.items():
                try:
                    f.result()
                    logger.info(f"Topic {topic} creado o ya existe")
                except Exception as e:
                    logger.warning(f"Error creando topic {topic}: {e}")
        except Exception as e:
            logger.error(f"Error en admin de Kafka: {e}")
    
    def flush(self, timeout: float = 10.0) -> None:
        """Fuerza el flush de mensajes pendientes.
        
        Args:
            timeout: Tiempo máximo de espera en segundos.
        """
        if self._producer:
            remaining = self._producer.flush(timeout)
            if remaining > 0:
                logger.warning(f"{remaining} mensajes pendientes tras flush")
    
    def close(self) -> None:
        """Cierra el productor y libera recursos."""
        self.flush()
        if self._producer:
            self._producer = None
            logger.info("Productor Kafka cerrado")

// === ARCHIVO: app/infrastructure/adapters/kafka_consumer.py ===
import logging
import asyncio
from typing import Optional, Callable, Awaitable
from uuid import UUID

from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class MessageHandler:
    """Interfaz para manejar mensajes procesados."""
    
    async def handle(self, event: TransactionEvent) -> None:
        """Procesa un evento de transacción."""
        raise NotImplementedError


class KafkaConsumerAdapter:
    """Adaptador para consumir eventos desde Apache Kafka.
    
    Implementa el patrón de adaptador para el puerto EventConsumer.
    Maneja la deserialización de eventos, manejo de offsets y
    rebalanceo de particiones.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._consumer: Optional[Consumer] = None
        self._running = False
        self._handlers: dict[EventType, MessageHandler] = {}
        self._init_consumer()
    
    def _init_consumer(self) -> None:
        """Inicializa el consumidor de Kafka con configuración de alto throughput."""
        config = {
            'bootstrap.servers': self._settings.kafka_bootstrap_servers,
            'group.id': self._settings.kafka_consumer_group,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'auto.commit.interval.ms': 5000,
            'max.poll.interval.ms': 300000,
            'session.timeout.ms': 10000,
            'heartbeat.interval.ms': 3000,
            'fetch.min.bytes': 1,
            'fetch.max.wait.ms': 500,
            'max.partition.fetch.bytes': 1048576,
        }
        self._consumer = Consumer(config)
        logger.info(f"Consumidor Kafka inicializado para grupo {self._settings.kafka_consumer_group}")
    
    def register_handler(self, event_type: EventType, handler: MessageHandler) -> None:
        """Registra un handler para un tipo de evento específico.
        
        Args:
            event_type: Tipo de evento a manejar.
            handler: Instancia que procesará el evento.
        """
        self._handlers[event_type] = handler
        logger.info(f"Handler registrado para evento {event_type.value}")
    
    def _deserialize_event(self, message) -> Optional[TransactionEvent]:
        """Deserializa un mensaje de Kafka en un evento de dominio.
        
        Args:
            message: Mensaje raw de Kafka.
            
        Returns:
            Evento de dominio o None si la deserialización falla.
        """
        try:
            event_data = message.value().decode('utf-8')
            event_dict = TransactionEvent.model_validate_json(event_data)
            
            event_type = event_dict.event_type
            if event_type == EventType.TRANSACTION_INITIATED:
                return TransactionInitiated.model_validate_json(event_data)
            elif event_type == EventType.TRANSACTION_COMPLETED:
                return TransactionCompleted.model_validate_json(event_data)
            elif event_type == EventType.TRANSACTION_FAILED:
                return TransactionFailed.model_validate_json(event_data)
            else:
                logger.warning(f"Tipo de evento desconocido: {event_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error deserializando evento: {e}")
            return None
    
    async def _process_message(self, message) -> None:
        """Procesa un mensaje individual del topic.
        
        Args:
            message: Mensaje de Kafka a procesar.
        """
        event = self._deserialize_event(message)
        if event is None:
            logger.warning("Evento no deserializado, saltando mensaje")
            return
        
        handler = self._handlers.get(event.event_type)
        if handler is None:
            logger.debug(f"No hay handler para evento tipo {event.event_type.value}")
            return
        
        try:
            await handler.handle(event)
            logger.info(f"Evento {event.event_type.value} procesado para transacción {event.transaction_id}")
        except Exception as e:
            logger.error(f"Error procesando evento: {e}")
            raise
    
    async def start_consuming(self) -> None:
        """Inicia el loop de consumo de mensajes."""
        if self._consumer is None:
            logger.error("Consumidor Kafka no inicializado")
            return
        
        self._consumer.subscribe([self._settings.kafka_topic_transactions])
        self._running = True
        
        logger.info(f"Iniciando consumo del topic {self._settings.kafka_topic_transactions}")
        
        while self._running:
            try:
                msg = self._consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug(f"Fin de partición {msg.partition()}")
                        continue
                    else:
                        logger.error(f"Error de Kafka: {msg.error()}")
                        continue
                
                await self._process_message(msg)
                
                self._consumer.commit(asynchronous=False)
                
            except KafkaException as e:
                logger.error(f"Excepción de Kafka: {e}")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error en loop de consumo: {e}")
                await asyncio.sleep(1)
    
    def stop_consuming(self) -> None:
        """Detiene el consumo de mensajes."""
        self._running = False
        logger.info("Consumidor Kafka deteniendo consumo")
    
    def close(self) -> None:
        """Cierra el consumidor y libera recursos."""
        self.stop_consuming()
        if self._consumer:
            self._consumer.close()
            self._consumer = None
            logger.info("Consumidor Kafka cerrado")
    
    async def get_partition_info(self, topic: str) -> dict:
        """Obtiene información de particiones para un topic.
        
        Args:
            topic: Nombre del topic.
            
        Returns:
            Diccionario con información de particiones.
        """
        admin_client = AdminClient({
            'bootstrap.servers': self._settings.kafka_bootstrap_servers
        })
        
        cluster_metadata = admin_client.list_topics(topic=topic, timeout=10)
        partitions_info = {}
        
        if topic in cluster_metadata.topics:
            topic_metadata = cluster_metadata.topics[topic]
            for partition in topic_metadata.partitions.values():
                partitions_info[partition.id] = {
                    'leader': partition.leader,
                    'replicas': partition.replicas,
                    'isrs': partition.isrs,
                }
        
        return partitions_info

// === ARCHIVO: app/infrastructure/adapters/rabbitmq_producer.py ===
import logging
import json
import pika
from typing import Optional
from uuid import UUID

from app.domain.events import (
    TransactionEvent,
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    EventType,
)
from app.infrastructure.config.settings import Settings

logger = logging.getLogger(__name__)


class RabbitMQProducerAdapter:
    """Adaptador para publicar mensajes en RabbitMQ.
    
    Implementa el patrón de adaptador para publicar eventos en colas
    de RabbitMQ. Utiliza confirmación de publicación y manejo de
    conexiones para garantizar la entrega.
    """
    
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
        self._exchanges = {
            EventType.TRANSACTION_INITIATED: settings.rabbitmq_exchange_transactions,
            EventType.TRANSACTION_COMPLETED: settings.rabbitmq_exchange_transactions,
            EventType.TRANSACTION_FAILED: settings.rabbitmq_exchange_transactions,
        }
        self._init_connection()
    
    def _init_connection(self) -> None:
        """Inicializa la conexión a RabbitMQ con configuración robusta."""
        credentials = pika.PlainCredentials(
            self._settings.rabbitmq_username,
            self._settings.rabbitmq_password,
        )
        
        parameters = pika.ConnectionParameters(
            host=self._settings.rabbitmq_host,
            port=self._settings.rabbitmq_port,
            virtual_host=self._settings.rabbitmq_vhost,
            credentials=credentials,
            connection_attempts=3,
            retry_delay=1,
            socket_timeout=5,
            heartbeat=60,
            blocked_connection_timeout=300,
        )
        
        try:
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._channel.confirm_delivery()
            self._declare_exchanges_and_queues()
            logger.info(f"Conexión RabbitMQ establecida hacia {self._settings.rabbitmq_host}:{self._settings.rabbitmq_port}")
        except Exception as e:
            logger.error(f"Error conectando a RabbitMQ: {e}")
            raise
    
    def _declare_exchanges_and_queues(self) -> None:
        """Declara los exchanges y colas necesarios."""
        if self._channel is None:
            return
        
        self._channel.exchange_declare(
            exchange=self._settings.rabbitmq_exchange_transactions,
            exchange_type='topic',
            durable=True,
            auto_delete=False,
        )
        
        for event_type in EventType:
            queue_name = f"{self._settings.rabbitmq_queue_prefix}{event_type.value}"
            routing_key = event_type.value
            
            self._channel.queue_declare(
                queue=queue_name,
                durable=True,
                exclusive=False,
                auto_delete=False,
            )
            
            self._channel.queue_bind(
                exchange=self._settings.rabbitmq_exchange_transactions,
                queue=queue_name,
                routing_key=routing_key,
            )
            
            logger.info(f"Cola {queue_name} vinculada al exchange con routing key {routing_key}")
    
    def _serialize_event(self, event: TransactionEvent) -> str:
        """Serializa un evento a JSON para transmisión.
        
        Args:
            event: Evento de dominio a serializar.
            
        Returns:
            Representación JSON del evento.
        """
        return event.model_dump_json()
    
    def _on_publish_confirmation(self, method) -> None:
        """Callback para confirmaciones de publicación.
        
        Args:
            method: Método de confirmación de RabbitMQ.
        """
        if method.reply_code == 200:
            logger.debug(f"Publicación confirmada: {method.reply_code}")
        else:
            logger.warning(f"Publicación no confirmada: {method.reply_code} - {method.reply_text}")
    
    async def publish(self, event: TransactionEvent) -> bool:
        """Publica un evento en RabbitMQ.
        
        Args:
            event: Evento de dominio a publicar.
            
        Returns:
            True si el evento se publicó exitosamente, False en caso contrario.
        """
        if self._channel is None or self._connection is None or self._connection.is_closed:
            logger.error("Conexión RabbitMQ no disponible")
            self._reconnect()
            return False
        
        try:
            exchange = self._exchanges.get(event.event_type)
            routing_key = event.event_type.value
            message_body = self._serialize_event(event)
            
            properties = pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2,
                message_id=event.transaction_id,
                timestamp=int(event.occurred_at.timestamp()) if event.occurred_at else None,
                headers={
                    'event_type': event.event_type.value,
                    'transaction_id': str(event.transaction_id),
                },
            )
            
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message_body,
                properties=properties,
                mandatory=True,
            )
            
            logger.info(f"Evento {event.event_type.value} publicado para transacción {event.transaction_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error publicando en RabbitMQ: {e}")
            return False
    
    async def publish_batch(self, events: list[TransactionEvent]) -> int:
        """Publica un lote de eventos de forma eficiente.
        
        Args:
            events: Lista de eventos a publicar.
            
        Returns:
            Número de eventos publicados exitosamente.
        """
        success_count = 0
        for event in events:
            if await self.publish(event):
                success_count += 1
        
        logger.info(f"Publicados {success_count}/{len(events)} eventos del lote")
        return success_count
    
    def _reconnect(self) -> None:
        """Reconecta a RabbitMQ si la conexión se perdió."""
        try:
            if self._connection and not self._connection.is_closed:
                self._connection.close()
            self._init_connection()
            logger.info("Reconexión a RabbitMQ exitosa")
        except Exception as e:
            logger.error(f"Error en reconexión: {e}")
    
    def close(self) -> None:
        """Cierra la conexión y libera recursos."""
        if self._channel:
            try:
                self._channel.close()
            except Exception:
                pass
            self._channel = None
        
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
        
        logger.info("Conexión RabbitMQ cerrada")

// === ARCHIVO: app/infrastructure/adapters/rabbitmq_consumer.py ===
import json
import logging
import threading
from typing import Callable, Optional
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import ValidationError

from app.infrastructure.messaging.event_serializer import EventSerializer
from app.domain.events import (
    TransactionInitiated,
    TransactionCompleted,
    TransactionFailed,
    DomainEvent,
)

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    """Consumidor de mensajes RabbitMQ para eventos de transacciones.
    
    Implementa patrón de reconnect automático y manejo de errores.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        queue_name: str = "transaction_events",
        exchange_name: str = "transactions",
        routing_key: str = "transaction.#",
        prefetch_count: int = 10,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.prefetch_count = prefetch_count
        
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[BlockingChannel] = None
        self._serializer = EventSerializer()
        self._consuming = False
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 5
        self._reconnect_delay = 5
        self._lock = threading.Lock()
        self._event_handler: Optional[Callable[[DomainEvent], None]] = None

    def connect(self) -> None:
        """Establece conexión con RabbitMQ."""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
            connection_attempts=3,
            retry_delay=1,
        )
        
        try:
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._setup_exchange_and_queue()
            self._channel.basic_qos(prefetch_count=self.prefetch_count)
            self._reconnect_attempts = 0
            logger.info(
                f"Conectado a RabbitMQ en {self.host}:{self.port}"
            )
        except Exception as e:
            logger.error(f"Error al conectar a RabbitMQ: {e}")
            self._handle_connection_error(e)
            raise

    def _setup_exchange_and_queue(self) -> None:
        """Configura el exchange, cola y bindings."""
        if not self._channel:
            raise RuntimeError("Canal no inicializado")
        
        self._channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type="topic",
            durable=True,
        )
        
        self._channel.queue_declare(
            queue=self.queue_name,
            durable=True,
            arguments={
                "x-message-ttl": 86400000,
                "x-dead-letter-exchange": f"{self.exchange_name}.dlx",
                "x-dead-letter-routing-key": "dead-letter",
            },
        )
        
        self._channel.queue_bind(
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key,
        )
        
        logger.info(
            f"Exchange '{self.exchange_name}' y cola '{self.queue_name}' configurados"
        )

    def register_handler(
        self, handler: Callable[[DomainEvent], None]
    ) -> None:
        """Registra el handler para procesar eventos."""
        self._event_handler = handler

    def start_consuming(self) -> None:
        """Inicia el consumo de mensajes."""
        if not self._channel:
            raise RuntimeError("Canal no inicializado. Llama a connect() primero.")
        
        self._consuming = True
        self._channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._on_message,
            auto_ack=False,
        )
        
        logger.info(f"Iniciando consumo de '{self.queue_name}'...")
        
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Consumo interrumpido por usuario")
            self.stop_consuming()
        except Exception as e:
            logger.error(f"Error en el ciclo de consumo: {e}")
            self._handle_connection_error(e)
            raise

    def _on_message(
        self,
        channel: BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        """Callback para procesar mensajes recibidos."""
        try:
            event = self._deserialize_message(body, properties)
            
            if self._event_handler:
                self._event_handler(event)
            
            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.debug(f"Evento procesado: {event.event_type}")
            
        except ValidationError as e:
            logger.error(f"Error de validación del evento: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def _deserialize_message(
        self,
        body: bytes,
        properties: pika.spec.BasicProperties,
    ) -> DomainEvent:
        """Deserializa el mensaje según su tipo."""
        content_type = properties.content_type or "application/json"
        
        if content_type != "application/json":
            raise ValueError(f"Content type no soportado: {content_type}")
        
        message_data = json.loads(body.decode("utf-8"))
        event_type = message_data.get("event_type")
        
        return self._serializer.deserialize(message_data, event_type)

    def _handle_connection_error(self, error: Exception) -> None:
        """Maneja errores de conexión con reintentos."""
        with self._lock:
            if self._reconnect_attempts >= self._max_reconnect_attempts:
                logger.error(
                    f"Máximo de reintentos alcanzado. Error: {error}"
                )
                raise
            
            self._reconnect_attempts += 1
            logger.warning(
                f"Reintentando conexión ({self._reconnect_attempts}/{self._max_reconnect_attempts}) "
                f"en {self._reconnect_delay}s..."
            )

    def stop_consuming(self) -> None:
        """Detiene el consumo de mensajes."""
        self._consuming = False
        if self._channel and self._channel.is_open:
            self._channel.stop_consuming()
        logger.info("Consumo detenido")

    def close(self) -> None:
        """Cierra la conexión con RabbitMQ."""
        self.stop_consuming()
        
        if self._channel and self._channel.is_open:
            self._channel.close()
            logger.info("Canal de RabbitMQ cerrado")
        
        if self._connection and self._connection.is_open:
            self._connection.close()
            logger.info("Conexión a RabbitMQ cerrada")

    def __enter__(self) -> "RabbitMQConsumer":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

// === ARCHIVO: app/infrastructure/messaging/event_serializer.py ===
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

// === ARCHIVO: app/infrastructure/repositories/transaction_repository_impl.py ===
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

// === ARCHIVO: app/infrastructure/config/aws_config.py ===
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class AWSConfig(BaseSettings):
    """
    Configuración centralizada para servicios AWS utilizados en el sistema.
    
    Gestiona credenciales, regiones y parámetros de conexión para SQS,
    EventBridge y otros servicios AWS requeridos por la arquitectura EDA.
    """
    
    aws_access_key_id: str = Field(
        default_factory=lambda: os.getenv("AWS_ACCESS_KEY_ID", ""),
        description="ID de clave de acceso AWS"
    )
    
    aws_secret_access_key: str = Field(
        default_factory=lambda: os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        description="Clave de acceso secreta AWS"
    )
    
    aws_region: str = Field(
        default_factory=lambda: os.getenv("AWS_REGION", "us-east-1"),
        description="Región AWS por defecto"
    )
    
    sqs_queue_url: str = Field(
        default_factory=lambda: os.getenv("SQS_QUEUE_URL", ""),
        description="URL de la cola SQS principal"
    )
    
    sqs_max_retries: int = Field(
        default=3,
        description="Máximo de reintentos para operaciones SQS"
    )
    
    sqs_visibility_timeout: int = Field(
        default=30,
        description="Tiempo de invisibilidad del mensaje en segundos"
    )
    
    sqs_wait_time_seconds: int = Field(
        default=20,
        description="Tiempo de espera largo para polling de mensajes"
    )
    
    eventbridge_bus_name: str = Field(
        default_factory=lambda: os.getenv("EVENTBRIDGE_BUS_NAME", "default"),
        description="Nombre del Event Bus"
    )
    
    use_localstack: bool = Field(
        default_factory=lambda: os.getenv("USE_LOCALSTACK", "false").lower() == "true",
        description="Usar LocalStack para desarrollo local"
    )
    
    localstack_endpoint: Optional[str] = Field(
        default_factory=lambda: os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566"),
        description="Endpoint de LocalStack"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


aws_config = AWSConfig()


# =============================================================================
# POLÍTICAS IAM COMENTADAS (referencia para configuración en producción)
# =============================================================================
#
# Política mínima para productor SQS:
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "sqs:SendMessage",
#                 "sqs:SendMessageBatch",
#                 "sqs:GetQueueUrl",
#                 "sqs:GetQueueAttributes"
#             ],
#             "Resource": "arn:aws:sqs:{region}:{account}:{queue-name}"
#         }
#     ]
# }
#
# Política mínima para consumidor SQS:
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "sqs:ReceiveMessage",
#                 "sqs:DeleteMessage",
#                 "sqs:ChangeMessageVisibility",
#                 "sqs:GetQueueUrl",
#                 "sqs:GetQueueAttributes"
#             ],
#             "Resource": "arn:aws:sqs:{region}:{account}:{queue-name}"
#         }
#     ]
# }
#
# Política para EventBridge:
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "events:PutEvents"
#             ],
#             "Resource": "arn:aws:events:{region}:{account}:event-bus/{bus-name}"
#         }
#     ]
# }
#
# =============================================================================


def get_boto3_client_kwargs() -> dict:
    """
    Retorna los argumentos de configuración para clientes boto3.
    
    Detecta si se debe usar LocalStack para desarrollo local
    o AWS real para producción.
    """
    kwargs = {
        "region_name": aws_config.aws_region,
    }
    
    if aws_config.aws_access_key_id and aws_config.aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_config.aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_config.aws_secret_access_key
    
    if aws_config.use_localstack:
        kwargs["endpoint_url"] = aws_config.localstack_endpoint
    
    return kwargs


def validate_aws_configuration() -> bool:
    """
    Valida que la configuración de AWS esté completa para entornos de producción.
    
    Returns:
        True si la configuración es válida, False en caso contrario.
    """
    if aws_config.use_localstack:
        return True
    
    if not aws_config.aws_access_key_id or not aws_config.aws_secret_access_key:
        return False
    
    if not aws_config.sqs_queue_url:
        return False
    
    return True

// === ARCHIVO: app/infrastructure/adapters/aws_sqs_producer.py ===
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.infrastructure.config.aws_config import (
    aws_config,
    get_boto3_client_kwargs,
)
from app.domain.events import TransactionEvent, EventType
from app.domain.entities.transaction import Transaction


logger = logging.getLogger(__name__)


class SQSMessagingError(Exception):
    """Excepción específica para errores de mensajería SQS."""
    pass


class AWSSQSProducer:
    """
    Adaptador para publicar mensajes en AWS SQS.
    
    Implementa el patrón de puerto definido en la capa de dominio,
    serializando eventos de dominio y enviándolos a la cola configurada.
    Maneja reintentos automáticos y logging detallado para trazabilidad.
    """
    
    def __init__(
        self,
        queue_url: Optional[str] = None,
        max_retries: Optional[int] = None,
    ):
        """
        Inicializa el productor SQS.
        
        Args:
            queue_url: URL de la cola SQS (usa configuración si no se provee).
            max_retries: Máximo de reintentos en caso de error.
        """
        self._queue_url = queue_url or aws_config.sqs_queue_url
        self._max_retries = max_retries or aws_config.sqs_max_retries
        self._client = None
        self._connect()
    
    def _connect(self) -> None:
        """
        Establece la conexión con el servicio SQS.
        
        Raises:
            SQSMessagingError: Si no se puede establecer conexión.
        """
        try:
            client_kwargs = get_boto3_client_kwargs()
            self._client = boto3.client("sqs", **client_kwargs)
            logger.info(
                "Productor SQS inicializado correctamente",
                extra={
                    "queue_url": self._queue_url,
                    "region": aws_config.aws_region,
                    "use_localstack": aws_config.use_localstack,
                }
            )
        except Exception as e:
            logger.error("Error al inicializar cliente SQS", extra={"error": str(e)})
            raise SQSMessagingError(f"Error al inicializar cliente SQS: {e}")
    
    def _serialize_message(self, event: TransactionEvent) -> dict:
        """
        Serializa el evento de dominio para su envío a SQS.
        
        Args:
            event: Evento de dominio a serializar.
            
        Returns:
            Diccionario con el mensaje serializado.
        """
        return {
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event.event_type.value,
            "payload": event.model_dump(),
        }
    
    def publish_transaction_event(
        self,
        transaction: Transaction,
        event_type: EventType,
    ) -> str:
        """
        Publica un evento de transacción en la cola SQS.
        
        Args:
            transaction: Transacción que originó el evento.
            event_type: Tipo de evento a publicar.
            
        Returns:
            ID del mensaje publicado.
            
        Raises:
            SQSMessagingError: Si falla después de todos los reintentos.
        """
        event = TransactionEvent.from_transaction(transaction, event_type)
        message_body = self._serialize_message(event)
        
        return self._send_message(
            message_body=json.dumps(message_body, default=str),
            deduplication_id=transaction.is_idempotent_key(),
            attributes={
                "event_type": event_type.value,
                "transaction_id": str(transaction.id),
                "timestamp": message_body["timestamp"],
            },
        )
    
    def _send_message(
        self,
        message_body: str,
        deduplication_id: Optional[str] = None,
        attributes: Optional[dict] = None,
    ) -> str:
        """
        Envía el mensaje a SQS con manejo de reintentos.
        
        Args:
            message_body: Cuerpo del mensaje en formato JSON.
            deduplication_id: ID para idempotencia (FIFO queue).
            attributes: Atributos de mensaje adicionales.
            
        Returns:
            ID del mensaje publicado.
            
        Raises:
            SQSMessagingError: Si falla después de todos los reintentos.
        """
        last_error = None
        
        for attempt in range(1, self._max_retries + 1):
            try:
                send_kwargs = {
                    "QueueUrl": self._queue_url,
                    "MessageBody": message_body,
                }
                
                if deduplication_id:
                    send_kwargs["MessageDeduplicationId"] = deduplication_id
                    send_kwargs["MessageGroupId"] = "transaction-processing"
                
                if attributes:
                    send_kwargs["MessageAttributes"] = {
                        key: {"StringValue": value, "DataType": "String"}
                        for key, value in attributes.items()
                    }
                
                response = self._client.send_message(**send_kwargs)
                message_id = response["MessageId"]
                
                logger.info(
                    "Mensaje publicado en SQS",
                    extra={
                        "message_id": message_id,
                        "queue_url": self._queue_url,
                        "attempt": attempt,
                    }
                )
                
                return message_id
                
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "Unknown")
                last_error = e
                
                logger.warning(
                    "Error al enviar mensaje a SQS",
                    extra={
                        "error_code": error_code,
                        "error_message": str(e),
                        "attempt": attempt,
                        "max_retries": self._max_retries,
                    }
                )
                
                if attempt == self._max_retries:
                    break
                    
            except BotoCoreError as e:
                last_error = e
                logger.warning(
                    "Error de conexión al enviar mensaje a SQS",
                    extra={
                        "error": str(e),
                        "attempt": attempt,
                    }
                )
                
                if attempt == self._max_retries:
                    break
        
        error_msg = (
            f"Error al publicar mensaje en SQS después de {self._max_retries} intentos: "
            f"{last_error}"
        )
        logger.error(error_msg)
        raise SQSMessagingError(error_msg)
    
    def publish_raw_message(
        self,
        message_body: dict,
        deduplication_id: Optional[str] = None,
    ) -> str:
        """
        Publica un mensaje raw sin envolver en evento de dominio.
        
        Útil para mensajes de sistema o eventos externos.
        
        Args:
            message_body: Diccionario con el contenido del mensaje.
            deduplication_id: ID para idempotencia.
            
        Returns:
            ID del mensaje publicado.
        """
        return self._send_message(
            message_body=json.dumps(message_body, default=str),
            deduplication_id=deduplication_id,
        )
    
    def get_queue_attributes(self) -> dict:
        """
        Obtiene atributos de la cola SQS.
        
        Returns:
            Diccionario con los atributos de la cola.
        """
        try:
            response = self._client.get_queue_attributes(
                QueueUrl=self._queue_url,
                AttributeNames=["All"]
            )
            return response.get("Attributes", {})
        except ClientError as e:
            logger.error("Error al obtener atributos de cola SQS", extra={"error": str(e)})
            raise SQSMessagingError(f"Error al obtener atributos de cola: {e}")
    
    def close(self) -> None:
        """
        Cierra la conexión con el servicio SQS.
        """
        if self._client:
            self._client = None
            logger.info("Conexión SQS cerrada")

// === ARCHIVO: app/infrastructure/adapters/aws_sqs_consumer.py ===
import json
import logging
from datetime import datetime
from typing import Any, Callable, List, Optional
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.infrastructure.config.aws_config import (
    aws_config,
    get_boto3_client_kwargs,
)
from app.domain.events import TransactionEvent, EventType


logger = logging.getLogger(__name__)


@dataclass
class SQSMessage:
    """
    Representa un mensaje recibido de SQS con metadatos.
    """
    message_id: str
    receipt_handle: str
    body: dict
    attributes: dict
    message_attributes: dict
    

class SQSConsumerError(Exception):
    """Excepción específica para errores del consumidor SQS."""
    pass


class AWSSQSConsumer:
    """
    Adaptador para consumir mensajes desde AWS SQS.
    
    Implementa el patrón de consumidor de eventos del dominio,
    manejando el ciclo de vida completo: recepción, procesamiento,
    confirmación y manejo de errores. Soporta polling largo y
    procesamiento por lotes.
    """
    
    def __init__(
        self,
        queue_url: Optional[str] = None,
        max_number_of_messages: int = 10,
        wait_time_seconds: Optional[int] = None,
        visibility_timeout: Optional[int] = None,
    ):
        """
        Inicializa el consumidor SQS.
        
        Args:
            queue_url: URL de la cola SQS.
            max_number_of_messages: Número máximo de mensajes por recepción.
            wait_time_seconds: Tiempo de espera para polling largo.
            visibility_timeout: Tiempo de invisibilidad del mensaje.
        """
        self._queue_url = queue_url or aws_config.sqs_queue_url
        self._max_messages = max_number_of_messages
        self._wait_time = wait_time_seconds or aws_config.sqs_wait_time_seconds
        self._visibility_timeout = visibility_timeout or aws_config.sqs_visibility_timeout
        self._client = None
        self._running = False
        self._connect()
    
    def _connect(self) -> None:
        """
        Establece la conexión con el servicio SQS.
        
        Raises:
            SQSConsumerError: Si no se puede establecer conexión.
        """
        try:
            client_kwargs = get_boto3_client_kwargs()
            self._client = boto3.client("sqs", **client_kwargs)
            logger.info(
                "Consumidor SQS inicializado correctamente",
                extra={
                    "queue_url": self._queue_url,
                    "region": aws_config.aws_region,
                    "max_messages": self._max_messages,
                    "wait_time": self._wait_time,
                }
            )
        except Exception as e:
            logger.error("Error al inicializar cliente SQS", extra={"error": str(e)})
            raise SQSConsumerError(f"Error al inicializar cliente SQS: {e}")
    
    def _parse_message(self, raw_message: dict) -> SQSMessage:
        """
        Parsea un mensaje raw de SQS a formato estructurado.
        
        Args:
            raw_message: Mensaje recibido de SQS.
            
        Returns:
            Objeto SQSMessage parseado.
        """
        body = json.loads(raw_message.get("Body", "{}"))
        
        attributes = {
            "sent_timestamp": raw_message.get("Attributes", {}).get("SentTimestamp"),
            "approximate_receive_count": raw_message.get("Attributes", {}).get("ApproximateReceiveCount"),
            "approximate_first_receive_timestamp": raw_message.get("Attributes", {}).get("ApproximateFirstReceiveTimestamp"),
        }
        
        message_attributes = {
            key: value.get("StringValue")
            for key, value in raw_message.get("MessageAttributes", {}).items()
        }
        
        return SQSMessage(
            message_id=raw_message.get("MessageId", ""),
            receipt_handle=raw_message.get("ReceiptHandle", ""),
            body=body,
            attributes=attributes,
            message_attributes=message_attributes,
        )
    
    def receive_messages(
        self,
        max_messages: Optional[int] = None,
    ) -> List[SQSMessage]:
        ""
        Recibe mensajes de la cola SQS usando polling largo.
        
        Args:
            max_messages: Número máximo de mensajes a recibir.
            
        Returns:
            Lista de mensajes recibidos.
            
        Raises:
            SQSConsumerError: Si falla la recepción de mensajes.
        """
        max_num = max_messages or self._max_messages
        
        try:
            response = self._client.receive_message(
                QueueUrl=self._queue_url,
                MaxNumberOfMessages=max_num,
                WaitTimeSeconds=self._wait_time,
                VisibilityTimeout=self._visibility_timeout,
                MessageAttributeNames=["All"],
                AttributeNames=["All"],
            )
            
            messages = response.get("Messages", [])
            
            if messages:
                logger.info(
                    f"Recibidos {len(messages)} mensajes de SQS",
                    extra={"queue_url": self._queue_url}
                )
            
            return [self._parse_message(msg) for msg in messages]
            
        except ClientError as e:
            logger.error("Error al recibir mensajes de SQS", extra={"error": str(e)})
            raise SQSConsumerError(f"Error al recibir mensajes: {e}")
        
        except BotoCoreError as e:
            logger.error("Error de conexión al recibir mensajes", extra={"error": str(e)})
            raise SQSConsumerError(f"Error de conexión: {e}")
    
    def delete_message(self, receipt_handle: str) -> bool:
        """
        Elimina un mensaje de la cola después de procesarlo exitosamente.
        
        Args:
            receipt_handle: Handle del mensaje a eliminar.
            
        Returns:
            True si se eliminó correctamente.
            
        Raises:
            SQSConsumerError: Si falla la eliminación.
        """
        try:
            self._client.delete_message(
                QueueUrl=self._queue_url,
                ReceiptHandle=receipt_handle,
            )
            
            logger.debug(
                "Mensaje eliminado de la cola",
                extra={"receipt_handle": receipt_handle[:20] + "..."}
            )
            return True
            
        except ClientError as e:
            logger.error(
                "Error al eliminar mensaje de SQS",
                extra={"error": str(e), "receipt_handle": receipt_handle[:20] + "..."}
            )
            raise SQSConsumerError(f"Error al eliminar mensaje: {e}")
    
    def change_visibility_timeout(
        self,
        receipt_handle: str,
        timeout_seconds: int,
    ) -> bool:
        """
        Cambia el tiempo de invisibilidad de un mensaje.
        
        Útil cuando el procesamiento toma más tiempo del esperado
        para evitar que el mensaje vuelva a la cola.
        
        Args:
            receipt_handle: Handle del mensaje.
            timeout_seconds: Nuevo timeout en segundos.
            
        Returns:
            True si se cambió correctamente.
        """
        try:
            self._client.change_message_visibility(
                QueueUrl=self._queue_url,
                ReceiptHandle=receipt_handle,
                VisibilityTimeout=timeout_seconds,
            )
            
            logger.debug(
                "Visibilidad del mensaje cambiada",
                extra={
                    "timeout_seconds": timeout_seconds,
                    "receipt_handle": receipt_handle[:20] + "...",
                }
            )
            return True
            
        except ClientError as e:
            logger.error(
                "Error al cambiar visibilidad del mensaje",
                extra={"error": str(e)}
            )
            return False
    
    def process_messages(
        self,
        handler: Callable[[SQSMessage], bool],
        max_iterations: Optional[int] = None,
    ) -> int:
        """
        Procesa mensajes de la cola ejecutando el handler proporcionado.
        
        El handler debe retornar True si el mensaje fue procesado
        exitosamente (y se elimina de la cola) o False si hubo
        un error temporal (el mensaje vuelve a estar disponible).
        
        Args:
            handler: Función que procesa cada mensaje.
            max_iterations: Número máximo de iteraciones de polling.
            
        Returns:
            Número de mensajes procesados exitosamente.
        """
        processed_count = 0
        iteration = 0
        
        while self._running:
            iteration += 1
            
            if max_iterations and iteration > max_iterations:
                logger.info("Límite de iteraciones alcanzado")
                break
            
            try:
                messages = self.receive_messages()
                
                if not messages:
                    continue
                
                for message in messages:
                    try:
                        success = handler(message)
                        
                        if success:
                            self.delete_message(message.receipt_handle)
                            processed_count += 1
                        else:
                            logger.warning(
                                "Handler retornó False, mensaje no eliminado",
                                extra={"message_id": message.message_id}
                            )
                            
                    except Exception as e:
                        logger.error(
                            "Error al procesar mensaje",
                            extra={
                                "message_id": message.message_id,
                                "error": str(e),
                            }
                        )
                        
            except SQSConsumerError as e:
                logger.error("Error en ciclo de procesamiento", extra={"error": str(e)})
                
        return processed_count
    
    def start_consuming(
        self,
        handler: Callable[[SQSMessage], bool],
    ) -> None:
        """
        Inicia el ciclo de consumo continuo de mensajes.
        
        Args:
            handler: Función que procesa cada mensaje.
        """
        self._running = True
        logger.info("Iniciando consumo de mensajes SQS")
        
        try:
            self.process_messages(handler)
        finally:
            self._running = False
            logger.info("Ciclo de consumo detenido")
    
    def stop_consuming(self) -> None:
        """
        Detiene el ciclo de consumo de mensajes.
        """
        self._running = False
        logger.info("Solicitud de parada de consumidor recibida")
    
    def get_queue_attributes(self) -> dict:
        """
        Obtiene atributos de la cola SQS.
        
        Returns:
            Diccionario con los atributos de la cola.
        """
        try:
            response = self._client.get_queue_attributes(
                QueueUrl=self._queue_url,
                AttributeNames=["All"]
            )
            return response.get("Attributes", {})
        except ClientError as e:
            logger.error("Error al obtener atributos de cola SQS", extra={"error": str(e)})
            raise SQSConsumerError(f"Error al obtener atributos de cola: {e}")
    
    def get ApproximateNumberOfMessages(self) -> int:
        """
        Obtiene el número aproximado de mensajes en la cola.
        
        Returns:
            Número de mensajes aproximados.
        """
        attributes = self.get_queue_attributes()
        return int(attributes.get("ApproximateNumberOfMessages", "0"))
    
    def close(self) -> None:
        """
        Cierra la conexión con el servicio SQS.
        """
        self._running = False
        if self._client:
            self._client = None
            logger.info("Conexión SQS cerrada")

// === ARCHIVO: tests/unit/test_transaction_usecase.py ===
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

// === ARCHIVO: tests/integration/test_kafka_integration.py ===
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
import json

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.events import TransactionInitiated, TransactionCompleted, EventType
from app.infrastructure.adapters.kafka_producer import KafkaProducerAdapter
from app.infrastructure.messaging.event_serializer import EventSerializer


class TestKafkaIntegration:
    """Tests de integración para validar la comunicación con Kafka."""

    @pytest.fixture
    def sample_transaction(self):
        """Crea una transacción de ejemplo para las pruebas."""
        return Transaction(
            id=uuid4(),
            account_id=uuid4(),
            amount=Decimal("500.00"),
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_kafka_producer(self):
        """Mock del producer de Kafka."""
        with patch('confluent_kafka.Producer') as mock_prod:
            mock_instance = MagicMock()
            mock_prod.return_value = mock_instance
            yield mock_instance

    @pytest.mark.asyncio
    async def test_kafka_producer_publish_event(self, sample_transaction, mock_kafka_producer):
        """Verifica que el producer publique eventos en Kafka correctamente."""
        event = TransactionInitiated.from_transaction(sample_transaction, EventType.INITIATED)
        serializer = EventSerializer()
        serialized = serializer.serialize(event)

        producer = KafkaProducerAdapter(
            bootstrap_servers='localhost:9092',
            topic='transaction.events'
        )

        await producer.publish('transaction.events', event)

        mock_kafka_producer.produce.assert_called_once()
        call_args = mock_kafka_producer.produce.call_args
        assert call_args[1]['topic'] == 'transaction.events'

    @pytest.mark.asyncio
    async def test_kafka_consumer_receives_message(self):
        """Verifica que el consumer reciba mensajes de Kafka."""
        from app.infrastructure.adapters.kafka_consumer import KafkaConsumerAdapter

        with patch('confluent_kafka.Consumer') as mock_cons:
            mock_instance = MagicMock()
            mock_cons.return_value = mock_instance

            mock_message = MagicMock()
            mock_message.value.return_value = json.dumps({
                'transaction_id': str(uuid4()),
                'event_type': 'INITIATED',
                'amount': '500.00'
            }).encode('utf-8')
            mock_message.error.return_value = None

            mock_instance.consume.return_value = [mock_message]

            consumer = KafkaConsumerAdapter(
                bootstrap_servers='localhost:9092',
                topic='transaction.events',
                group_id='test-group'
            )

            messages = []
            async for msg in consumer.consume():
                messages.append(msg)
                if len(messages) >= 1:
                    break

            assert len(messages) == 1

    @pytest.mark.asyncio
    async def test_kafka_event_serialization(self, sample_transaction):
        """Verifica la serialización de eventos para Kafka."""
        event = TransactionInitiated.from_transaction(sample_transaction, EventType.INITIATED)
        serializer = EventSerializer()

        serialized = serializer.serialize(event)

        assert isinstance(serialized, bytes)
        assert 'transaction_id' in serialized.decode('utf-8')
        assert 'event_type' in serialized.decode('utf-8')

        deserialized = serializer.deserialize(serialized)
        assert deserialized.transaction_id == str(sample_transaction.id)

    @pytest.mark.asyncio
    async def test_kafka_producer_error_handling(self, mock_kafka_producer):
        """Verifica el manejo de errores del producer de Kafka."""
        mock_kafka_producer.produce.side_effect = Exception("Kafka broker unavailable")

        producer = KafkaProducerAdapter(
            bootstrap_servers='localhost:9092',
            topic='transaction.events'
        )

        event = TransactionInitiated(
            transaction_id=str(uuid4()),
            event_type=EventType.INITIATED,
            timestamp=datetime.now().isoformat()
        )

        with pytest.raises(Exception):
            await producer.publish('transaction.events', event)

    @pytest.mark.asyncio
    async def test_kafka_idempotent_producer(self, sample_transaction):
        """Verifica la idempotencia del producer de Kafka."""
        from app.infrastructure.adapters.kafka_producer import KafkaProducerAdapter

        with patch('confluent_kafka.Producer') as mock_prod:
            mock_instance = MagicMock()
            mock_prod.return_value = mock_instance

            producer = KafkaProducerAdapter(
                bootstrap_servers='localhost:9092',
                topic='transaction.events',
                enable_idempotence=True
            )

            event = TransactionCompleted.from_transaction(sample_transaction, EventType.COMPLETED)

            await producer.publish('transaction.events', event)
            await producer.publish('transaction.events', event)

            assert mock_instance.produce.call_count == 2

// === ARCHIVO: tests/integration/test_rabbitmq_integration.py ===
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from decimal import Decimal
from datetime import datetime
import json

from app.domain.entities.transaction import Transaction, TransactionStatus, TransactionType
from app.domain.events import TransactionFailed, EventType
from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter
from app.infrastructure.messaging.event_serializer import EventSerializer


class TestRabbitMQIntegration:
    """Tests de integración para validar la comunicación con RabbitMQ."""

    @pytest.fixture
    def sample_failed_transaction(self):
        """Crea una transacción fallida de ejemplo para las pruebas."""
        return Transaction(
            id=uuid4(),
            account_id=uuid4(),
            amount=Decimal("-100.00"),
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.FAILED,
            failure_reason="Fondos insuficientes",
            created_at=datetime.now()
        )

    @pytest.fixture
    def mock_rabbitmq_connection(self):
        """Mock de la conexión a RabbitMQ."""
        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel
            yield mock_channel

    @pytest.mark.asyncio
    async def test_rabbitmq_producer_publish_event(self, sample_failed_transaction, mock_rabbitmq_connection):
        """Verifica que el producer publique eventos en RabbitMQ correctamente."""
        event = TransactionFailed.from_transaction(
            sample_failed_transaction,
            EventType.FAILED
        )

        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events'
        )

        await producer.publish('transaction.events', event)

        mock_rabbitmq_connection.basic_publish.assert_called_once()
        call_args = mock_rabbitmq_connection.basic_publish.call_args
        assert call_args[1]['exchange'] == ''
        assert call_args[1]['routing_key'] == 'transaction.events'

    @pytest.mark.asyncio
    async def test_rabbitmq_consumer_receives_message(self):
        """Verifica que el consumer reciba mensajes de RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_consumer import RabbitMQConsumerAdapter

        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel

            test_message = {
                'transaction_id': str(uuid4()),
                'event_type': 'FAILED',
                'amount': '100.00'
            }

            mock_channel.basic_consume.return_value = None

            consumer = RabbitMQConsumerAdapter(
                host='localhost',
                port=5672,
                queue='transaction.events'
            )

            messages = []

            def on_message_callback(ch, method, properties, body):
                messages.append(json.loads(body))
                ch.basic_ack(delivery_tag=method.delivery_tag)

            mock_channel.basic_consume = AsyncMock()
            mock_channel.basic_consume.side_effect = on_message_callback

            with patch('pika.SelectConnection'):
                pass

    @pytest.mark.asyncio
    async def test_rabbitmq_event_serialization(self, sample_failed_transaction):
        """Verifica la serialización de eventos para RabbitMQ."""
        event = TransactionFailed.from_transaction(
            sample_failed_transaction,
            EventType.FAILED
        )
        serializer = EventSerializer()

        serialized = serializer.serialize(event)

        assert isinstance(serialized, bytes)
        decoded = json.loads(serialized.decode('utf-8'))
        assert decoded['transaction_id'] == str(sample_failed_transaction.id)
        assert decoded['event_type'] == 'FAILED'

    @pytest.mark.asyncio
    async def test_rabbitmq_producer_confirm_delivery(self, mock_rabbitmq_connection):
        """Verifica la confirmación de entrega de mensajes en RabbitMQ."""
        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events',
            confirm_delivery=True
        )

        mock_rabbitmq_connection.confirm_delivery.assert_not_called()

        await producer.publish('transaction.events', MagicMock())

    @pytest.mark.asyncio
    async def test_rabbitmq_dead_letter_queue(self):
        """Verifica el manejo de dead letter queue en RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter

        with patch('pika.BlockingConnection') as mock_conn:
            mock_channel = MagicMock()
            mock_conn.return_value.channel.return_value = mock_channel

            producer = RabbitMQProducerAdapter(
                host='localhost',
                port=5672,
                queue='transaction.events',
                dead_letter_queue='transaction.events.dlq'
            )

            mock_channel.queue_declare.assert_called()

            dlq_call = mock_channel.queue_declare.call_args_list[1]
            assert 'transaction.events.dlq' in str(dlq_call)

    @pytest.mark.asyncio
    async def test_rabbitmq_retry_mechanism(self, mock_rabbitmq_connection):
        """Verifica el mecanismo de reintentos en RabbitMQ."""
        from app.infrastructure.adapters.rabbitmq_producer import RabbitMQProducerAdapter

        mock_rabbitmq_connection.basic_publish.side_effect = [
            Exception("Connection error"),
            None
        ]

        producer = RabbitMQProducerAdapter(
            host='localhost',
            port=5672,
            queue='transaction.events',
            retry_attempts=3,
            retry_delay=1
        )

        event = TransactionFailed(
            transaction_id=str(uuid4()),
            event_type=EventType.FAILED,
            timestamp=datetime.now().isoformat(),
            failure_reason="Error de conexión"
        )

        with patch('asyncio.sleep', new_callable=AsyncMock):
            await producer.publish('transaction.events', event)

        assert mock_rabbitmq_connection.basic_publish.call_count == 2
```
