import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # prevent Uvicorn from being shut off
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(name)s | %(asctime)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "level": "INFO",
        }
    },
}

def setup_logging():
    dictConfig(LOGGING_CONFIG)

def get_logger(name: str):
    return logging.get_logger(name)