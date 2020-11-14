import logging
from os import environ

from colorlog import ColoredFormatter

_LOG_LEVEL = (
    logging.NOTSET
    if not environ.get('LOG_LEVEL')
    and bool(environ.get('LOGGING')) is not True
    else environ.get('LOG_LEVEL')
)


_LOG_FORMAT = environ.get('LOG_FORMAT') or (
    '%(asctime)s %(log_color)s%(levelname)-7s%(reset)s | '
    '[%(name)s:%(funcName)s:%(lineno)d] %(log_color)s%'
    '(message)s%(reset)s'
)  # noqa: E501
'''

_LOG_FORMAT = environ.get('LOG_FORMAT') or (
    '%(asctime)s %(log_color)s%(levelname)-7s%(reset)s | '
    '%(message)s%(reset)s' ) # noqa: E501
'''


def get_logger(name=__name__):
    logging.root.setLevel(_LOG_LEVEL or logging.INFO)
    formatter = ColoredFormatter(
        _LOG_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        },
    )
    stream = logging.StreamHandler()
    stream.setLevel(environ.get('LOG_LEVEL') or logging.INFO)
    stream.setFormatter(formatter)
    log_ = logging.getLogger(name)
    log_.setLevel(environ.get('LOG_LEVEL') or logging.INFO)
    log_.addHandler(stream)
    return log_
