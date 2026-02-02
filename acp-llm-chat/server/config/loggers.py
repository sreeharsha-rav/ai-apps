import logging
import contextvars
from logging.config import dictConfig

# This context var should match the one in middleware
request_id_var = contextvars.ContextVar("request_id", default="n/a")

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get()
        return True

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": RequestIdFilter,
        },
    },
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | [%(request_id)s] | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "llm-chat": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("llm-chat")
