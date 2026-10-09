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