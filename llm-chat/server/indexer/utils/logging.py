import logging
import sys
from typing import Optional


def setup_logger(
        name: str,
        level: int = logging.INFO,
        log_format: Optional[str] = None,
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the given name and configuration.

    Args:
        name: The name of the logger
        level: The logging level (default is logging.INFO)
        log_format: Custom log format (optional)
        log_to_console: Whether to log to console (default is True)
        log_to_file: Whether to log to file (default is False)
        log_file_path: Path to log file (required if log_to_file is True)

    Returns:
        logging.Logger: The configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers if they already exist
    if logger.handlers:
        return logger

    # Default format if not specified
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(log_format)

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_to_file:
        if not log_file_path:
            raise ValueError("log_file_path must be provided when log_to_file is True")

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger