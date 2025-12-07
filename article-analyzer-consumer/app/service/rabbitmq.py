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
from app.logger import log  # Make sure logger.py is set up correctly
from app.core.config import settings  # Make sure core.config is set up correctly

# Import dependencies for message processing
from app.service.spk import ResponseHandler  # Adjust import path as needed
from app.db.db import insert_into_entire_table, upsert_validation_failed_article  # Adjust import path as needed
from app.service.validation import Evaluation  # Adjust import path as needed

# Initialize message processing components (outside the class)
response = ResponseHandler()
evaluator = Evaluation()


@dataclass
class RabbitMQConfig:
    host: str = 'localhost'
    port: int = 5672
    username: str = 'guest'
    password: str = 'guest'
    virtual_host: str = '/'


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
                # if attempt == retries:
                #     stacktrace = traceback.format_exc()
                    # error = SysErrorModel(  # Assumes SysErrorModel and mail_utils are defined elsewhere
                    #     type="RabbitMQ Connection Error",
                    #     message="Failed to reconnect after several attempts.",
                    #     stack_trace=stacktrace
                    # )
                    # mail_utils.system_error_alert(error.dict())

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



def message_callback(ch: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    """
    This function will act as the callback when a message is received.
    Here, you would add your message processing logic.
    """
    try:
        # Decode bytes to string
        body_str = body.decode('utf-8')

        # Convert JSON string to dictionary
        body_dict = json.loads(body_str)

        # Call the method with the dictionary  # Assuming Response is a class
        input_data = body_dict['body']
        newspaper_id = body_dict['newspaper_id']
        article_id = body_dict['article_id']
        ai_resp = response.extraction(input_data, 0)
        if ai_resp:
            output_json = json.loads(ai_resp)
            validation_score = 4
            # validation_reasoning_output, validation_score = evaluator.evaluate(input_data, output_json)
            if validation_score > 3:
                header = body_dict['header']
                sector = body_dict['sector']
                # link_to_article = body_dict['link_to_article']
                link_to_article = "https://www.ft.com/content/3e5b75b4-7259-413a-9483-5c5613423ad7"
                insert_into_entire_table(output_json, article_id, newspaper_id, header, link_to_article, sector)
                log.log_info(f"Article analyzed, parsed and inserted into db, article_id {article_id}")
            else:
                log.log_warning(f"Parsed article's validation score below threshold, for the article {article_id}")
                upsert_validation_failed_article(article_id=article_id, newspaper_id=newspaper_id)
        else:
            log.log_warning("No response received from the AI model. The article has been inserted into the 'failed_article' table in the database.")

        # Acknowledge message
        log.log_info("Consumed message acknowledged")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError as e:
        # Acknowledge the message, even if JSON decoding fails
        log.log_error(f"JSON Decode Error: Invalid message format in message {body.decode()}. Error: {e}", exception=e)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge and remove from the queue on error
    except Exception as e:
        log.log_error("Error processing message", exception=e)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge and move to DLQ


def start_consumer(queue_name: str, fail_exchange: str, fail_routing_key: str): # added fail exchange and routing key
    while True:
        try:
            channel = rabbitmq_connection.get_fresh_channel()
            if not channel:
                raise Exception("Channel not available.") #Generic exception cause i dont have the rabbitmq connection one

            # queue_args = {
            #     "x-dead-letter-exchange": fail_exchange,
            #     "x-dead-letter-routing-key": fail_routing_key
            # }

            # # Declare queue with dead-letter settings
            # channel.queue_declare(queue=queue_name, durable=True, arguments=queue_args)
            
            channel.queue_declare(queue=queue_name, durable=True)
            
            channel.basic_qos(prefetch_count=1)  # Ensure only one message is processed at a time

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
            # channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # requeue on failure
            try:
                rabbitmq_connection.reconnect()
            except Exception as err:
                log.log_error(f"Reconnect failed: {err}")
                # stacktrace = ''.join(traceback.format_exception(*sys.exc_info()))
                # sys_error = SysErrorModel( # Assumes SysErrorModel and mail_utils are defined elsewhere
                #     type="RabbitMQ Consumer Reconnect Error",
                #     message="Unable to reconnect RabbitMQ consumer",
                #     stack_trace=stacktrace
                # )
                # mail_utils.system_error_alert(sys_error.dict())
            time.sleep(20)  # prevent tight loop on failure

        except Exception as e:
            log.log_error("Unexpected error in RabbitMQ consumer", exception=e)
            # channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # requeue on failure
            time.sleep(3)


def run_consumer_in_thread(queue_name: str, fail_exchange: str, fail_routing_key: str): # added fail exchange and routing key
    thread = threading.Thread(target=start_consumer, args=(queue_name, fail_exchange, fail_routing_key,), daemon=True) # added fail exchange and routing key
    thread.start()


# Create the RabbitMQ connection instance
rabbitmq_connection = RabbitMQConnection(RabbitMQConfig(
    host=settings.rabbitmq.HOST,
    port=settings.rabbitmq.PORT,
    username=settings.rabbitmq.USER,
    password=settings.rabbitmq.PASSWORD,
    virtual_host='/'
))

# Start the consumer thread
# run_consumer_in_thread(
#     queue_name=settings.rabbitmq.SPOKESPERSON_ARTICLE_ANALYZER_QUEUE,  # Replace with the actual queue name from settings
#     fail_exchange='', # replace with fail exchange
#     fail_routing_key='' # replace with fail routing key
# )