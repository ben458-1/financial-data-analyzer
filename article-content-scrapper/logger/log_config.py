import logging
import logging.config
import os
import sys
from core.config import data_source

# import logger.mail_log
# from logging.handlers import RotatingFileHandler, SMTPHandler


# This variable will track whether the configuration has been initialized
logg = None


# Define a function to set up logging
def setup_logging(default_level=logging.INFO):
    global logg
    if logg is None:
        """Setup logging configuration."""
        # Create a directory for logs if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(f'{log_dir}', exist_ok=True)

        # Define logging configuration
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
                'verbose': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d'
                },
                'simple': {
                    'format': '%(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'level': logging.INFO,
                    'stream': sys.stdout,
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'level': logging.INFO,
                    'filename': f'{log_dir}/app.log',
                    'maxBytes': 10 * 1024 * 1024,  # 10 MB
                    'backupCount': 5,
                },
                'mail': {
                    'class': 'logger.log_mail.SMTPLOGHandler',
                    'level': data_source.EMAIL_ALERT_LEVEL,
                    'formatter': 'verbose',
                    'mailhost': (data_source.SMTP_HOST, data_source.SMTP_PORT),
                    'fromaddr': data_source.SENDER_EMAIL,
                    'toaddrs': data_source.DEV_RECIPIENT_EMAILS.split(','),
                    'subject': 'Application Error',
                    # 'credentials': ('username', 'password'),
                    # 'secure': (),
                },
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['console', 'file', 'mail'],
                    'level': default_level,
                    'propagate': True,
                },
            },
        }

        # Apply logging configuration
        logging.config.dictConfig(logging_config)
        logg = logging
        return logg
    else:
        return logg


if __name__ == '__main__':
    setup_logging()
