import configparser
from configparser import ConfigParser
from threading import Lock
import os


# Singleton Config Manager
class ConfigManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of ConfigManger exists
        :param args:
        :param kwargs:
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
                    # Get the directory of the current file
                    cur_dir = os.path.dirname(os.path.abspath(__file__))
                    app_conf_file_path = os.path.join(cur_dir, 'application.ini')  # Use os.path.join for portability
                    cls._instance._initialize(app_config_file=app_conf_file_path)
        return cls._instance

    def _initialize(self, app_config_file="application.ini"):
        """
                Initialize the ConfigManager with the given config file.
                """

        self.app_config = ConfigParser(os.environ, interpolation=configparser.ExtendedInterpolation())
        self.app_config.read(app_config_file)
        self.db_params = self.get_db_param()
        self.mq_params = self.get_mq_param()
        self.ARTICLE_URL_EXCHANGE = self.app_config.get('MQ', 'article-url_exchange')
        self.ARTICLE_URL_QUEUE = self.app_config.get('MQ', 'article-url_queue')
        self.ARTICLE_URL_KEY = self.app_config.get('MQ', 'article-url_key')
        self.mq_connection_attempt = int(self.app_config.get('MQ', 'connection_attempts'))
        self.mq_retry_delay = int(self.app_config.get('MQ', 'retry_delay'))
        self.mq_delivery_mode = int(self.app_config.get('MQ', 'delivery_mode'))

    def get_db_param(self):
        if self.app_config.has_section('DB'):
            db = {'host': self.app_config.get('DB', 'host'),
                  'database': self.app_config.get('DB', 'database'),
                  'user': self.app_config.get('DB', 'user'),
                  'password': self.app_config.get('DB', 'password')
                  }
        else:
            raise Exception('Section DB not found in the application.ini file')
        return db

    def get_mq_param(self):
        mq = {'host': self.app_config.get('MQ', 'host'),
              'port': self.app_config.get('MQ', 'port'),
              'username': self.app_config.get('MQ', 'username'),
              'password': self.app_config.get('MQ', 'password')
              }
        return mq


config_manager = ConfigManager()
