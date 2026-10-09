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