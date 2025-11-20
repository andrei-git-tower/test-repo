"""
Unit tests for the logger module.
"""

import unittest
import logging
import os
import shutil
from pathlib import Path
from logger import setup_logger, get_logger, ColoredFormatter


class TestColoredFormatter(unittest.TestCase):
    """Test cases for the ColoredFormatter class."""

    def setUp(self):
        self.formatter = ColoredFormatter('%(levelname)s - %(message)s')

    def test_format_includes_color_codes(self):
        """Test that formatter adds ANSI color codes to log records."""
        record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
        formatted = self.formatter.format(record)
        self.assertIn('\033[', formatted)  # Should contain ANSI codes

    def test_format_all_levels(self):
        """Test formatting for all log levels."""
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in levels:
            record = logging.LogRecord(
                name='test',
                level=getattr(logging, level),
                pathname='test.py',
                lineno=1,
                msg='Test message',
                args=(),
                exc_info=None
            )
            formatted = self.formatter.format(record)
            self.assertIsInstance(formatted, str)
            self.assertIn('Test message', formatted)


class TestLoggerSetup(unittest.TestCase):
    """Test cases for logger setup and configuration."""

    def setUp(self):
        self.test_log_dir = 'test_logs'
        self.logger_name = 'test_logger'

    def tearDown(self):
        # Clean up test logs
        if os.path.exists(self.test_log_dir):
            shutil.rmtree(self.test_log_dir)

        # Remove handlers from logger
        logger = logging.getLogger(self.logger_name)
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def test_setup_logger_creates_instance(self):
        """Test that setup_logger returns a valid logger instance."""
        logger = setup_logger(self.logger_name, log_dir=self.test_log_dir)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, self.logger_name)

    def test_setup_logger_creates_log_directory(self):
        """Test that setup_logger creates the log directory if it doesn't exist."""
        self.assertFalse(os.path.exists(self.test_log_dir))
        setup_logger(self.logger_name, log_dir=self.test_log_dir)
        self.assertTrue(os.path.exists(self.test_log_dir))

    def test_setup_logger_adds_handlers(self):
        """Test that setup_logger adds both console and file handlers."""
        logger = setup_logger(self.logger_name, log_dir=self.test_log_dir)
        self.assertEqual(len(logger.handlers), 2)

        handler_types = [type(h).__name__ for h in logger.handlers]
        self.assertIn('StreamHandler', handler_types)
        self.assertIn('RotatingFileHandler', handler_types)

    def test_setup_logger_respects_log_level(self):
        """Test that setup_logger sets the correct log level."""
        logger = setup_logger(self.logger_name, log_level='DEBUG', log_dir=self.test_log_dir)
        self.assertEqual(logger.level, logging.DEBUG)

        logger2 = setup_logger('logger2', log_level='ERROR', log_dir=self.test_log_dir)
        self.assertEqual(logger2.level, logging.ERROR)

    def test_setup_logger_prevents_duplicate_handlers(self):
        """Test that calling setup_logger multiple times doesn't create duplicate handlers."""
        logger1 = setup_logger(self.logger_name, log_dir=self.test_log_dir)
        initial_handler_count = len(logger1.handlers)

        logger2 = setup_logger(self.logger_name, log_dir=self.test_log_dir)
        self.assertEqual(len(logger2.handlers), initial_handler_count)

    def test_logger_writes_to_file(self):
        """Test that logger actually writes messages to log file."""
        logger = setup_logger(self.logger_name, log_level='DEBUG', log_dir=self.test_log_dir)
        test_message = 'This is a test log message'

        logger.info(test_message)

        # Force flush handlers
        for handler in logger.handlers:
            handler.flush()

        # Check if log file was created and contains the message
        log_files = list(Path(self.test_log_dir).glob('*.log'))
        self.assertGreater(len(log_files), 0)

        with open(log_files[0], 'r') as f:
            log_content = f.read()
            self.assertIn(test_message, log_content)

    def test_get_logger_returns_existing_logger(self):
        """Test that get_logger returns an existing logger instance."""
        setup_logger(self.logger_name, log_dir=self.test_log_dir)
        retrieved_logger = get_logger(self.logger_name)
        self.assertEqual(retrieved_logger.name, self.logger_name)


if __name__ == '__main__':
    unittest.main()
