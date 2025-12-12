"""
Logging module for CLI Tool.

This module provides a centralized logging system with multiple handlers,
custom formatters, and rotation capabilities for file logs.

Environment Variables:
    LOG_DIR: Directory for log files (default: 'logs')
    LOG_MAX_BYTES: Maximum size per log file in bytes (default: 10485760 = 10MB)
    LOG_BACKUP_COUNT: Number of backup files to retain (default: 5)

Example Usage:
    Basic setup:
        >>> from logger import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info('Application started')

    With custom configuration:
        >>> logger = setup_logger(__name__, log_level='DEBUG', log_dir='/var/log/myapp')
        >>> logger.debug('Debug information')
        >>> logger.warning('Warning message')

    Using environment variables:
        $ export LOG_DIR=/custom/logs
        $ export LOG_MAX_BYTES=20971520  # 20MB
        $ export LOG_BACKUP_COUNT=10
        $ python cli.py
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

# Configuration from environment variables
DEFAULT_LOG_DIR = os.getenv('LOG_DIR', 'logs')
DEFAULT_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10 * 1024 * 1024))  # 10MB
DEFAULT_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""

    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',   # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'
    }

    # Cache formatted level names for performance
    _cached_level_names = {}

    def format(self, record):
        # Use cached colored level name if available
        if record.levelname not in self._cached_level_names:
            log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            self._cached_level_names[record.levelname] = (
                f"{log_color}{record.levelname}{self.COLORS['RESET']}"
            )

        # Temporarily replace levelname with colored version
        original_levelname = record.levelname
        record.levelname = self._cached_level_names[original_levelname]
        result = super().format(record)
        record.levelname = original_levelname  # Restore original
        return result


def setup_logger(
    name: str,
    log_level: str = 'INFO',
    log_dir: str = None,
    max_bytes: int = None,
    backup_count: int = None
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name: Logger name (typically __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files (defaults to LOG_DIR env var or 'logs')
        max_bytes: Maximum size per log file (defaults to LOG_MAX_BYTES env var or 10MB)
        backup_count: Number of backup files to retain (defaults to LOG_BACKUP_COUNT env var or 5)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Use environment variable defaults if not specified
    log_dir = log_dir or DEFAULT_LOG_DIR
    max_bytes = max_bytes or DEFAULT_MAX_BYTES
    backup_count = backup_count or DEFAULT_BACKUP_COUNT

    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)

    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # File handler with rotation
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger instance."""
    return logging.getLogger(name)
