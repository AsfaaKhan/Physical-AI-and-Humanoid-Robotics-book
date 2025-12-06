import logging
import sys
from datetime import datetime
from utils.config import settings


def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Function to set up a logger with specified name and level
    """
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    """
    return setup_logger(name)


# Create a central logger configuration
def configure_logging():
    """
    Configure logging for the entire application
    """
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)

    # Set specific log levels for different modules
    logging.getLogger("uvicorn").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("google.generativeai").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("qdrant_client").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)


# Initialize logging
configure_logging()