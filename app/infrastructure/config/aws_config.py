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