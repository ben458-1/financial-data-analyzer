from logger.log_config import setup_logging
import time

# Call the setup_logging function
logging = setup_logging()
logg = logging.getLogger('Spokesperson')


def log_info(message, **kwargs):
    logg.info(message, extra=kwargs)


def log_warning(message, **kwargs):
    logg.warning(message, extra=kwargs)


def log_error(message, exception=None, **kwargs):
    if exception:
        logg.error(f'{message} : \n {exception}', exc_info=True, extra=kwargs)
    else:
        logg.error(message, extra=kwargs)


def log_critical(message, exception=None, **kwargs):
    if exception:
        logg.error(message, extra=kwargs)
    else:
        logg.critical(f'{message} : \n {exception}', exc_info=True, extra=kwargs)


def log_separator():
    logg.info('=======================================================================================')


def log_application_start():
    logg.info('============================ Application Start ========================================')


def log_application_end():
    """Log the application end event."""
    logg.info('=================================   ***   =============================================')


def log_application_shutdown():
    """Log an unexpected application shutdown event."""
    logg.warning('========================= Application Shutting down ================================')


def log_application_start_time():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logg.info(f'Application started at {start_time}')


def log_application_end_time():
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logg.info(f'Application ended at {end_time}')