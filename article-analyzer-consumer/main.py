# main.py
import os
import sys
import threading
import time
from app.logger import log
from app.core.config import settings
from app.service.rabbitmq import run_consumer_in_thread

# This is a good place to initialize things and start threads
def main():
    log.log_info("Starting application...")

    # Create the RabbitMQ connection instance
    # Ensure your settings are correctly loaded before this
    # rabbitmq_connection_instance = RabbitMQConnection(RabbitMQConfig(
    #     host=settings.rabbitmq.HOST,
    #     port=settings.rabbitmq.PORT,
    #     username=settings.rabbitmq.USER,
    #     password=settings.rabbitmq.PASSWORD,
    #     virtual_host='/'
    # ))

    # Start the consumer thread
    run_consumer_in_thread(
        queue_name=settings.rabbitmq.SPOKESPERSON_ARTICLE_ANALYZER_QUEUE,
        fail_exchange='',
        fail_routing_key=''
    )

    # Keep the main thread alive so daemon threads can run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.log_info("Application shutting down.")
        # Add shutdown logic here if needed, e.g., closing connections
        # rabbitmq_connection_instance.close()

if __name__ == "__main__":
    # Add the project root to sys.path if running directly,
    # though if you always run `python main.py` from project root, it's implicit.
    # This can help if you try to run it from a subfolder, though not ideal.
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # if current_dir not in sys.path:
    #     sys.path.append(current_dir)

    main()