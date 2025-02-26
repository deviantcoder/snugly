import logging

from django.utils import timezone


def send_log(logger, message, level='info'):
    """
    Sends a log message to the specified logger with the given log level.
    Args:
        logger (logging.Logger): The logger instance to which the message will be sent.
        message (str): The log message to be sent.
        level (str, optional): The log level for the message. Defaults to 'info'.
            Valid levels are 'debug', 'info', 'warning', 'error', and 'critical'.
    Raises:
        ValueError: If an invalid log level is provided.
    Example:
        send_log(logger, 'This is a test message', 'warning')
    """
    
    LEVEL_MAP = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    try:
        log_level = LEVEL_MAP[level.lower().strip()]
    except KeyError:
        raise ValueError(f'Invalid log level: {level}')
    
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f'{current_time}: {message}'

    logger.log(log_level, message)