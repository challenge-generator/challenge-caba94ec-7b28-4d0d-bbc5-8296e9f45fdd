# Diseño y Mantenimiento de Sistema EDA en Banca

La empresa de banca necesita implementar y mantener un sistema de arquitectura orientada a eventos (EDA) para procesar transacciones financieras en tiempo real. El sistema debe integrarse con Apache Kafka y RabbitMQ para garantizar la eficiencia y escalabilidad. Los eventos clave incluyen 'transacción iniciada', 'transacción completada' y 'error en transacción'. El sistema debe manejar un throughput de 5 000 transacciones por segundo con un SLA de 99.99%. Los eventos deben ser idempotentes y consistentes bajo condiciones de alta carga. El candidato debe decidir entre usar Kafka para el procesamiento de streaming y RabbitMQ para la gestión de colas, considerando trade-offs como latencia y complejidad de implementación.

## Informacion General

| Campo | Valor |
|-------|-------|
| **Tema** | Implementa y Mantiene de Sistemas EDA con Dominio de Kafka, RabbitMQ y más |
| **Nivel** | senior-l2 |
| **Tipo** | practical |
| **Tiempo estimado** | 15 horas |

## Fases del Reto

### Fase 0: Configuración del Proyecto

**Objetivo:** Obtener el proyecto base funcional enviando el Código Base a un asistente de IA, que lo analizará, corregirá errores y generará un ZIP listo para usar.

**Tiempo estimado:** 15-30 minutos

**Instrucciones:**

- Asegúrate de tener instalado para ejecutar el proyecto: Un IDE o editor de código.
- Copia todo el contenido del campo **Código Base** de este reto — incluyendo el texto de instrucciones que aparece al inicio.
- Abre un asistente de IA (Claude en claude.ai, ChatGPT o Gemini — se recomienda Claude), pega el contenido copiado en el chat y envíalo.
- El asistente analizará los archivos, corregirá errores y generará un archivo ZIP descargable. Descárgalo y extráelo en la carpeta donde quieras trabajar.
- Verifica que el proyecto arranca sin errores.

**Entregable:** El proyecto compila/arranca sin errores.

<details>
<summary>Pistas de conocimiento</summary>

- Copia el Código Base completo incluyendo el texto de instrucciones al inicio — esas instrucciones le indican al asistente exactamente qué hacer con los archivos.
- Si el asistente no genera el ZIP automáticamente al terminar el análisis, escríbele: "genera el ZIP ahora".
- Si el proyecto tiene errores al arrancar, comparte el mensaje de error con el mismo asistente para que lo corrija.

</details>

### Fase 1: Definición del Dominio y Requisitos

**Objetivo:** Establecer los requisitos del sistema y definir el dominio de las transacciones financieras.

**Tiempo estimado:** 3 horas

**Instrucciones:**

- Identificar los eventos clave del dominio y sus propiedades operativas.
- Definir los umbrales numéricos y las restricciones del sistema.
- Documentar los criterios de aceptación para la fase.

**Entregable:** Documento de requisitos del sistema con eventos definidos, umbrales y restricciones.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la idempotencia y consistencia de los eventos.
- Evalúa la latencia aceptable para el procesamiento de transacciones.

</details>

### Fase 2: Diseño del Sistema EDA

**Objetivo:** Diseñar la arquitectura del sistema EDA integrando Apache Kafka y RabbitMQ.

**Tiempo estimado:** 5 horas

**Instrucciones:**

- Decidir entre usar Kafka para el procesamiento de streaming y RabbitMQ para la gestión de colas.
- Documentar las decisiones de diseño y los trade-offs considerados.
- Definir los criterios de aceptación para la fase.

**Entregable:** Documento de diseño del sistema EDA con decisiones de integración y trade-offs documentados.

<details>
<summary>Pistas de conocimiento</summary>

- Evalúa la latencia y complejidad de implementación de Kafka y RabbitMQ.
- Considera la escalabilidad y fault tolerance del sistema.

</details>

### Fase 3: Implementación y Validación

**Objetivo:** Implementar el sistema EDA y validar su funcionamiento.

**Tiempo estimado:** 5 horas

**Instrucciones:**

- Implementar la integración de Kafka y RabbitMQ según el diseño.
- Realizar pruebas de carga y validar los umbrales numéricos y restricciones.
- Documentar los resultados y cualquier ajuste realizado.
- Definir los criterios de aceptación para la fase.

**Entregable:** Sistema EDA implementado y documentado con resultados de pruebas y ajustes.

<details>
<summary>Pistas de conocimiento</summary>

- Utiliza herramientas de prueba de carga para validar el throughput y SLA.
- Documenta cualquier ajuste realizado para cumplir con los criterios de aceptación.

</details>

### Fase 4: Mantenimiento y Optimización

**Objetivo:** Mantener y optimizar el sistema EDA para asegurar su eficiencia y escalabilidad a largo plazo.

**Tiempo estimado:** 2 horas

**Instrucciones:**

- Identificar áreas de mejora y optimización en el sistema.
- Implementar mejoras y documentar los cambios realizados.
- Realizar pruebas de regresión para asegurar la estabilidad del sistema.
- Definir los criterios de aceptación para la fase.

**Entregable:** Sistema EDA optimizado y documentado con cambios realizados y resultados de pruebas de regresión.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la latencia, throughput y fault tolerance en las áreas de mejora.
- Documenta los cambios y resultados de pruebas de regresión.

</details>

## Dimensiones Evaluadas

- **queEs**: ¿Qué es un sistema de arquitectura orientada a eventos (EDA) y cómo se integra con Apache Kafka y RabbitMQ?
- **paraQueSirve**: ¿Para qué sirve un sistema EDA en el dominio de las transacciones financieras?
- **comoSeUsa**: ¿Cómo se usa Apache Kafka y RabbitMQ en un sistema EDA?
- **erroresComunes**: ¿Cuáles son los errores comunes al implementar un sistema EDA y cómo se mitigan?
- **queDecisionesImplica**: ¿Qué decisiones implica la integración de Apache Kafka y RabbitMQ en un sistema EDA?

## Criterios de Evaluacion

- Definición clara de los requisitos del sistema y eventos del dominio.
- Diseño de la arquitectura EDA con decisiones de integración documentadas.
- Implementación y validación del sistema EDA con resultados documentados.
- Mantenimiento y optimización del sistema EDA con cambios documentados.

## Como trabajar con un asistente de IA

Hay dos caminos, elegi uno:

- **AGENTS.md** (recomendado) — instrucciones nativas del repo. Abri esta carpeta con tu agente local (Claude Code, Cursor, Codex, Copilot, Gemini) y las carga solo. Sabe que archivos faltan y con que comando se verifica, y completa el scaffold escribiendo en disco.
- **PROMPT_MEJORA.md** — para copiar y pegar en un chat (claude.ai, ChatGPT). Devuelve un ZIP con el proyecto. Sirve si no tenes un agente en el IDE.

Ninguno de los dos resuelve las fases del reto: eso es tu trabajo.

## Verificacion

El proyecto esta listo para trabajar cuando este comando corre sin errores:

```bash
pip install -r requirements.txt && python -c "import app.main"
```

---

*Reto generado automaticamente por Challenge Generator - Pragma*
