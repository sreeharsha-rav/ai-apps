import time
import logging
import logging.config
import uuid
import sys
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# ContextVar to hold request ID, ensuring async safety
request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)

class RequestIdFilter(logging.Filter):
    """
    Logging filter to inject request_id into log records from ContextVar.
    """
    def filter(self, record):
        record.request_id = request_id_ctx_var.get() or "-"
        return True

class ConsoleFormatter(logging.Formatter):
    """
    Custom formatter with colors for specific fields to mimic a production-ready standard output.
    Format: [TIME] [LEVEL] [REQ-ID] [LOGGER] MESSAGE
    """
    # ANSI Color Codes
    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    MAGENTA = "\x1b[35;20m"
    BLUE = "\x1b[34;20m"
    RESET = "\x1b[0m"

    def format(self, record):
        asctime = self.formatTime(record, self.datefmt)
        
        if record.levelno == logging.DEBUG:
            level_color = self.GREY
        elif record.levelno == logging.INFO:
            level_color = self.GREEN
        elif record.levelno == logging.WARNING:
            level_color = self.YELLOW
        elif record.levelno == logging.ERROR:
            level_color = self.RED
        elif record.levelno == logging.CRITICAL:
            level_color = self.BOLD_RED
        else:
            level_color = self.RESET

        # Formatting parts
        time_str = f"{self.CYAN}[{asctime}]{self.RESET}"
        level_str = f"{level_color}[{record.levelname}]{self.RESET}"
        req_id_str = f"{self.MAGENTA}[{getattr(record, 'request_id', '-') or '-'}]{self.RESET}"
        name_str = f"{self.BLUE}[{record.name}]{self.RESET}"
        
        # Message
        message = record.getMessage()
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            message += f"\n{record.exc_text}"
        
        return f"{time_str} {level_str} {req_id_str} {name_str} | {message}"

def configure_logging():
    """
    Configures logging using dictConfig.
    - Disables existing loggers to avoid duplicate/unformatted logs.
    - Sets up a central console handler with the custom formatter.
    - Re-routes uvicorn logs to use this formatter for consistency.
    """
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id_filter": {
                "()": RequestIdFilter,
            }
        },
        "formatters": {
            "default": {
                "()": ConsoleFormatter,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
                "filters": ["request_id_filter"],
            },
        },
        "loggers": {
            "root": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)


class LogRequestsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests and responses with execution time.
    Sets the request_id context variable for the duration of the request.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", f"req_{uuid.uuid4()}")
        token = request_id_ctx_var.set(request_id)
        
        start_time = time.time()
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"{request.method} - {request.url}")
            
            response = await call_next(request)
            
            process_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"Response: {response.status_code} "
                f"| Time: {process_time:.2f}ms"
            )
            
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url} "
                f"| Time: {process_time:.2f}ms",
                exc_info=True
            )
            raise e
            
        finally:
            request_id_ctx_var.reset(token)
