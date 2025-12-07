from db_service.db_handler import get_article_conf
import json
from mq_service.publisher import publish_message, establish_messaging_broker_connection
from conf.config_manager import config_manager


def message_dispatcher():
    print('Initiate to dispatching the message')
    EXCHANGE_NAME = config_manager.ARTICLE_URL_EXCHANGE
    ROUTING_KEY = config_manager.ARTICLE_URL_KEY
    connection = None

    article_configurations = get_article_conf()
    try:
        connection = establish_messaging_broker_connection()
        for ac in article_configurations:
            publish_message(connection, EXCHANGE_NAME, ROUTING_KEY, json.dumps(ac), ac.get('priority'))
        print('Publish successful')
    except Exception as e:
        print(e)
    finally:
        if connection is not None:
            # Close the connection
            connection.close()
            print('Messaging broker connection closed successfully')
