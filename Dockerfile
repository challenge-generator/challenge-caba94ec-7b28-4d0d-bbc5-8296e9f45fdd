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