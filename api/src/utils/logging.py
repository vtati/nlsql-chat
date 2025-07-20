"""
Logging configuration and utilities.
"""
import logging
import sys
from typing import Optional
from ..core.settings import settings


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up application logging configuration.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom log format string
    
    Returns:
        Configured logger instance
    """
    log_level = level or settings.log_level
    
    # Default format
    default_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=format_string or default_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger
    logger = logging.getLogger("nlsql")
    
    # Set specific loggers to appropriate levels
    if settings.is_development:
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("fastapi").setLevel(logging.DEBUG)
    else:
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(f"nlsql.{name}")


# Default logger instance
logger = setup_logging()