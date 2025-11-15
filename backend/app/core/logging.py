"""
Logging configuration for the application.
"""
import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger
from app.core.config import settings


def setup_logging():
    """Configure application logging with both console and file handlers."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("prepwise")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colored formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler with JSON formatting
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    file_handler.setFormatter(json_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logging()