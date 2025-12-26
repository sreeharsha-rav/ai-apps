import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG"
        },
        # "rotating_file": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": "src.log",
        #     "maxBytes": 10 * 1024 * 1024,  # 10 MB
        #     "backupCount": 2,
        #     "formatter": "json",
        #     "level": "INFO"
        # }
    },
    "loggers": {
        "src": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("llm-chat")
logger.setLevel(logging.DEBUG)
