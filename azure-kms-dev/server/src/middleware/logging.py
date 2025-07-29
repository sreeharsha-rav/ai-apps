import time
import uuid
import traceback
from datetime import datetime
import json
import logging
from logging.config import dictConfig
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # add exception information if available
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

# Define Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": JSONFormatter
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO"
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "src.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 2,
            "formatter": "json",
            "level": "INFO"
        }
    },
    "loggers": {
        "src": {
            "handlers": ["console", "rotating_file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("src")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # generate a unique request ID
        request_id = str(uuid.uuid4())

        # Store request ID in request state for use in endpoints
        request.state.request_id = request_id

        # FUTURE: add client info if needed

        # Log request details
        logger.info(
            f"[{request_id}] Incoming request: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": str(request.query_params),
                "headers": dict(request.headers),
                "event_type": "request_start"
            }
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Log successful response
            logger.info(
                f"[{request_id}] Response: {response.status_code} - {process_time_ms}ms",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time_ms": process_time_ms,
                    "event_type": "request_complete",
                    "success": True
                }
            )

            # Add timing headers to response
            response.headers["X-Process-Time"] = str(process_time_ms)
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            # Calculate timing for failed requests too
            process_time = time.perf_counter() - start_time
            process_time_ms = round(process_time * 1000, 2)

            # Log error with full traceback
            logger.error(
                f"[{request_id}] Request failed: {type(exc).__name__} - {process_time_ms}ms",
                extra={
                    "request_id": request_id,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "process_time_ms": process_time_ms,
                    "traceback": traceback.format_exc(),
                    "event_type": "request_error",
                    "success": False
                },
                exc_info=True
            )

            # Re-raise the exception to be handled by exception handlers
            raise exc