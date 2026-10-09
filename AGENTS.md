# AGENTS.md

Instrucciones para el agente de IA que abra este repositorio (Claude Code, Cursor, Codex, Copilot, Gemini). Se cargan solas: no hay que pegar nada en ningun chat.

## Que es este repositorio

Es el codigo base de un reto de aprendizaje de Pragma: **Diseño y Mantenimiento de Sistema EDA en Banca**.

| | |
|---|---|
| Tema | Implementa y Mantiene de Sistemas EDA con Dominio de Kafka, RabbitMQ y más |
| Nivel | senior-l2 |
| Chapter | Backend |
| Especialidad | Python |
| Stack | Python / FastAPI 0.115 |
| Patron arquitectonico | hexagonal/clean con enfoque reactivo para manejo de eventos |
| Tiempo estimado | 15 horas |

## Receta del stack

Esqueleto obligatorio:

- `pyproject.toml o requirements.txt en la raiz`
- `app/main.py con la instancia de FastAPI`
- `app/domain con entidades y puertos (Protocol o ABC)`
- `app/application con casos de uso`
- `app/infrastructure con repositorios y routers`

Dependencias:

- fastapi 0.115.0
- uvicorn 0.30.5
- pydantic 2.9.0
- sqlalchemy 2.0.32
- asyncpg 0.29.0
- confluent-kafka 2.5.0
- pika 1.3.2
- boto3 1.35.0
- pytest 8.2.2
- pytest-asyncio 0.24.0
- httpx 0.27.0
- docker n/a

## Tu tarea

Dejar este proyecto en estado **verificable**: que el comando de verificacion corra sin errores. Escribi los archivos en disco, en este repositorio. No generes ZIPs ni archivos adjuntos.

En orden:

1. Corre `pip install -r requirements.txt && python -c "import app.main"` y mira que falla.
2. Completa lo que falte de la lista de abajo: manifiesto de dependencias, punto de entrada, capa de interfaz y las capas del patron declarado.
3. Arregla SOLO los errores que impiden compilar o arrancar.
4. Volve a correr `pip install -r requirements.txt && python -c "import app.main"` hasta que pase.
5. Pará ahí.

## Regla dura: las fases son trabajo del humano

**PROHIBIDO implementar los entregables de las fases.** El valor del reto esta en que la persona los resuelva. Tu trabajo es que tenga un proyecto que arranca; el hueco pedagogico se queda como esta.

No resuelvas nada de esto:

- **Fase 1 — Definición del Dominio y Requisitos**: Documento de requisitos del sistema con eventos definidos, umbrales y restricciones.
- **Fase 2 — Diseño del Sistema EDA**: Documento de diseño del sistema EDA con decisiones de integración y trade-offs documentados.
- **Fase 3 — Implementación y Validación**: Sistema EDA implementado y documentado con resultados de pruebas y ajustes.
- **Fase 4 — Mantenimiento y Optimización**: Sistema EDA optimizado y documentado con cambios realizados y resultados de pruebas de regresión.

Distincion operativa:

- **Arreglar** (si): import faltante, tipo que no existe, dependencia sin declarar, error de sintaxis, archivo referenciado que no existe.
- **No tocar** (no): logica de negocio incompleta, validaciones ausentes, secretos hardcodeados, APIs deprecadas que funcionan, concurrencia insegura, patrones mejorables. Eso es lo que la persona tiene que encontrar.

## Lo que falta y tenes que completar

### 1. Boilerplate del stack (1)

Sin esto el proyecto no compila ni arranca. **Es tu trabajo crearlo**, y no toca nada de lo pedagogico: es andamiaje del stack.

- [ ] **__init__.py** — Sin __init__.py, app no es un paquete importable y "import app.main" falla.

### 2. Archivos que la arquitectura declara (1 de 24)

La propuesta arquitectonica del reto los lista y no llegaron al repo. Crealos con implementacion real, respetando la capa en la que viven:

- [ ] `README.md`

### 3. Referencias colgando (13)

Salieron de un analisis estatico del codigo que SI esta en el repo. Cada una rompe la compilacion:

- [ ] `app/main.py` — `EventConsumer.start`
      Se invoca `start` sobre `EventConsumer`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/main.py` — `EventConsumer.stop`
      Se invoca `stop` sobre `EventConsumer`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/usecases/process_transaction.py` — `TransactionRepository.info`
      Se invoca `info` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/usecases/process_transaction.py` — `TransactionRepository.error`
      Se invoca `error` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/usecases/process_transaction.py` — `TransactionRepository.warning`
      Se invoca `warning` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/usecases/process_transaction.py` — `TransactionRepository.debug`
      Se invoca `debug` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.info`
      Se invoca `info` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.warning`
      Se invoca `warning` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.debug`
      Se invoca `debug` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/application/handlers/transaction_event_handler.py` — `TransactionRepository.error`
      Se invoca `error` sobre `TransactionRepository`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.info`
      Se invoca `info` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.error`
      Se invoca `error` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `app/infrastructure/adapters/aws_sqs_producer.py` — `Transaction.warning`
      Se invoca `warning` sobre `Transaction`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

### Presentes (26)

- `pyproject.toml`
- `app/main.py`
- `app/infrastructure/config/settings.py`
- `app/domain/entities/transaction.py`
- `app/domain/events/__init__.py`
- `app/domain/ports/transaction_repository.py`
- `app/domain/ports/event_publisher.py`
- `app/domain/ports/event_consumer.py`
- `__init__.py`
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `app/application/usecases/process_transaction.py`
- `app/application/handlers/transaction_event_handler.py`
- `app/infrastructure/adapters/kafka_producer.py`
- `app/infrastructure/adapters/kafka_consumer.py`
- `app/infrastructure/adapters/rabbitmq_producer.py`
- `app/infrastructure/adapters/rabbitmq_consumer.py`
- `app/infrastructure/messaging/event_serializer.py`
- `app/infrastructure/repositories/transaction_repository_impl.py`
- `app/infrastructure/config/aws_config.py`
- `app/infrastructure/adapters/aws_sqs_producer.py`
- `app/infrastructure/adapters/aws_sqs_consumer.py`
- `tests/unit/test_transaction_usecase.py`
- `tests/integration/test_kafka_integration.py`
- `tests/integration/test_rabbitmq_integration.py`

### Capas del patron declarado

Cada una tiene que existir como directorio real con al menos un archivo. Codigo plano en la raiz no satisface el patron.

- `app`
- `app/domain`
- `app/domain/entities`
- `app/domain/events`
- `app/domain/ports`
- `app/application`
- `app/application/usecases`
- `app/application/handlers`
- `app/infrastructure`
- `app/infrastructure/adapters`
- `app/infrastructure/config`
- `app/infrastructure/messaging`
- `app/infrastructure/repositories`
- `tests`
- `tests/integration`
- `tests/unit`

## Verificacion

```bash
pip install -r requirements.txt && python -c "import app.main"
```

Ese comando pasando es la definicion de "terminado" para vos.

## Convenciones que tenes que respetar

- Un solo ecosistema: no declares librerias de otro lenguaje ni mezcles gestores de paquetes.
- Toda libreria que uses tiene que estar declarada en el manifiesto de dependencias.
- Todo import declarado tiene que usarse; todo tipo usado tiene que existir o venir de una dependencia declarada.
- El patron es **hexagonal/clean con enfoque reactivo para manejo de eventos**: los contratos (interfaces, puertos) los define la capa interna y los implementa la externa, nunca al revés.
- Los archivos que crees llevan implementacion real, no stubs: sin `TODO`, sin cuerpos vacios, sin `// getters y setters`.

## Contexto del candidato

Sirve para calibrar el nivel del codigo, no para resolver las fases.

- Perfil: Chapter Backend, Especialidad Desarrollador, Tecnología Python, Senior
- Brecha que el reto ataca: Implementa soluciones basada en arquitectura orientada a eventos (EDA) y tiene un sólido conocimiento de los conceptos relacionados con este tipo de arquitectura para implementar y mantener sistemas eficientes y escalables. Experiencia comprobable en al menos una herramienta como Apache Kafka, RabbitMQ, SQS, EventBridge, etc.
- Mision: Candidato Senior con experiencia en backend.

---

*Generado por Challenge Generator — Pragma. `README.md` tiene el enunciado completo del reto para la persona. `PROMPT_MEJORA.md` es la variante para pegar en un chat, si se prefiere ese flujo.*
