import pika
from conf.config_manager import config_manager


def publish_message(connection, exchange_name, routing_key, message, priority=5):
    try:

        channel = connection.channel()

        # Publish a message to the specified queue
        channel.basic_publish(
            exchange=exchange_name,  # Default exchange
            routing_key=routing_key,  # The name of the queue
            body=message,  # The message body
            properties=pika.BasicProperties(
                delivery_mode=config_manager.mq_delivery_mode,  # Make the message persistent
                priority=priority
            )
        )
    except Exception as e:
        print(e)


def establish_messaging_broker_connection():
    connection = None

    try:
        # Establish a connection to RabbitMQ server
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config_manager.mq_params.get('host'),
                                      port=config_manager.mq_params.get('port'),
                                      connection_attempts=config_manager.mq_connection_attempt,
                                      retry_delay=config_manager.mq_retry_delay)
        )
        return connection
    except Exception as e:
        print(e)
        if connection is not None:
            # Close the connection
            connection.close()
