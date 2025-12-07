import json
import sys
import time
import traceback
import threading
from dataclasses import dataclass
from typing import List

import pika
from pika.channel import Channel
from pika.exceptions import StreamLostError, ConnectionClosed
from pika.spec import Basic, BasicProperties

from core.config import data_source as ds
from exceptions.custom_exception import RabbitMQConnectionException
from logger import log
from service.utils import mail_utils
from service import article_crawler
from model.article_request import ArticleRequest
from model.system_error_mail import SysErrorModel


@dataclass
class RabbitMQConfig:
    host: str = 'localhost'
    port: int = 5672
    username: str = 'guest'
    password: str = 'guest'
    virtual_host: str = '/'


@dataclass
class RabbitMQQueueInfo:
    exchange: str = ''
    queue: str = ''
    routing_key: str = ''
    message: str = ''
    delivery_mode: int = 2
    priority: int = 5

    def display_info(self) -> str:
        return (
            f"RabbitMQ Queue Info:\n"
            f"  Exchange: {self.exchange}\n"
            f"  Queue: {self.queue}\n"
            f"  Routing Key: {self.routing_key}\n"
            f"  Message: {self.message}\n"
            f"  Delivery Mode: {self.delivery_mode}\n"
            f"  Priority: {self.priority}\n"
        )


class RabbitMQConnection:
    _instance = None
    _lock = threading.Lock()  # Ensure thread-safe singleton

    def __new__(cls, config: RabbitMQConfig):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: RabbitMQConfig):
        if self._initialized:
            log.log_info("Using existing RabbitMQ connection.")
            return

        self.config = config
        self.connection = None
        self.channel = None
        try:
            self._connect()
            log.log_info("New RabbitMQ Connection is established.")
            self._initialized = True
        except pika.exceptions.AMQPConnectionError as e:
            log.log_error("Initial RabbitMQ connection failed.", e)
            self.reconnect()

        log.log_info("New RabbitMQ Connection established.")

    def _connect(self):
        credentials = pika.PlainCredentials(self.config.username, self.config.password)
        parameters = pika.ConnectionParameters(
            host=self.config.host,
            port=self.config.port,
            credentials=credentials,
            virtual_host=self.config.virtual_host
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        log.log_info("RabbitMQ connection established.")

    def reconnect(self):
        retries = 5
        delay = 1
        for attempt in range(1, retries + 1):
            try:
                log.log_info(f"Reconnection attempt {attempt}...")
                time.sleep(delay)
                self._connect()
                return
            except pika.exceptions.AMQPConnectionError as e:
                log.log_error(f"Reconnect attempt {attempt} failed: {e}")
                delay *= 2
                if attempt == retries:
                    stacktrace = traceback.format_exc()
                    error = SysErrorModel(
                        type="RabbitMQ Connection Error",
                        message="Failed to reconnect after several attempts.",
                        stack_trace=stacktrace
                    )
                    mail_utils.system_error_alert(error.dict())

    def reset_connection(self):
        log.log_info("Resetting RabbitMQ connection.")
        self.close()
        self._initialized = False
        self._connect()

    def get_fresh_channel(self):
        if not self.connection or self.connection.is_closed:
            self.reconnect()
        if not self.channel or self.channel.is_closed:
            self.channel = self.connection.channel()
        return self.channel

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            log.log_warning("RabbitMQ connection closed.")


def publish_message(queue_info: RabbitMQQueueInfo):
    try:
        channel = rabbitmq_connection.channel
        if not channel:
            raise RabbitMQConnectionException()

        channel.basic_publish(
            exchange=queue_info.exchange,
            routing_key=queue_info.routing_key,
            body=queue_info.message,
            properties=pika.BasicProperties(
                delivery_mode=queue_info.delivery_mode,
                priority=queue_info.priority
            )
        )
        log.log_info(f"Message published to queue: {queue_info.queue}")
    except (ConnectionClosed, StreamLostError, ConnectionResetError) as e:
        log.log_error(f"Connection issue: {e}. Resetting and retrying...")
        rabbitmq_connection.reconnect()
        # Only retry the operation once after reconnecting
        if rabbitmq_connection.channel:  # Check if the connection is ready
            channel = rabbitmq_connection.channel
            channel.basic_publish(
                exchange=queue_info.exchange,
                routing_key=queue_info.routing_key,
                body=queue_info.message,
                properties=pika.BasicProperties(
                    delivery_mode=queue_info.delivery_mode,
                    priority=queue_info.priority
                )
            )
            log.log_info(f"Message published to queue after reconnecting: {queue_info.queue}")
    except Exception as e:
        log.log_error(f"Failed to publish message to {queue_info.queue}", exception=e)
        raise


def publish_message_into_article_analyzer(message: str):
    queue_info = RabbitMQQueueInfo(
        exchange=ds.SPOKESPERSON_ARTICLE_EXCHANGE,
        routing_key=ds.SPOKESPERSON_ARTICLE_CONTENT_ROUTING_KEY,
        queue=ds.SPOKESPERSON_ARTICLE_CONTENT_QUEUE,
        message=message
    )
    publish_message(queue_info)


def message_callback(ch: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    try:
        raw_data = body.decode()
        parsed_data = json.loads(raw_data)
        article_meta: List[ArticleRequest] = [ArticleRequest(**item) for item in parsed_data]

        log.log_info(f"Received {len(article_meta)} articles.")

        from service.article_crawler import extract_article_batch
        extract_article_batch(article_meta, publish=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        log.log_error("Error processing RabbitMQ message", exception=e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer(queue_name: str):
    while True:
        try:
            channel = rabbitmq_connection.get_fresh_channel()
            if not channel:
                raise RabbitMQConnectionException("Channel not available.")

            queue_args = {
                "x-dead-letter-exchange": ds.SPOKESPERSON_ARTICLE_FAIL_EXCHANGE,
                "x-dead-letter-routing-key": ds.SPOKESPERSON_ARTICLE_METADATA_FAIL_ROUTING_KEY
            }

            # Declare queue with dead-letter settings
            channel.queue_declare(queue=queue_name, durable=True, arguments=queue_args)

            # Ensure only one message is processed at a time
            channel.basic_qos(prefetch_count=1)

            # Bind callback function
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=message_callback,
                auto_ack=False
            )

            log.log_info(f"Started consumer on queue: {queue_name}")
            channel.start_consuming()  # Blocking call — exits only on failure

        except (ConnectionClosed, StreamLostError, ConnectionResetError) as e:
            log.log_error(f"Consumer connection issue: {e}. Attempting to reconnect...")
            try:
                rabbitmq_connection.reconnect()
            except Exception as err:
                log.log_error(f"Reconnect failed: {err}")
                stacktrace = ''.join(traceback.format_exception(*sys.exc_info()))
                sys_error = SysErrorModel(
                    type="RabbitMQ Consumer Reconnect Error",
                    message="Unable to reconnect RabbitMQ consumer",
                    stack_trace=stacktrace
                )
                mail_utils.system_error_alert(sys_error.dict())
            time.sleep(20)  # prevent tight loop on failure

        except Exception as e:
            log.log_error("Unexpected error in RabbitMQ consumer", exception=e)
            time.sleep(3)


def run_consumer_in_thread(queue_name: str):
    thread = threading.Thread(target=start_consumer, args=(queue_name,), daemon=True)
    thread.start()


# Create the RabbitMQ connection instance
rabbitmq_connection = RabbitMQConnection(RabbitMQConfig(
    host=ds.MQ_HOST,
    port=ds.MQ_PORT,
    username=ds.MQ_USER,
    password=ds.MQ_PASSWORD,
    virtual_host=ds.MQ_VIRTUAL_HOST
))

# Start the consumer thread
run_consumer_in_thread(ds.SPOKESPERSON_ARTICLE_METADATA_QUEUE)
