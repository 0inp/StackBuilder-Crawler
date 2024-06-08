import logging

from unittest.mock import patch

from src.adapters.db_logger import DBLoggerAdapter


class TestLoggerAdapter:
    @patch("sqlite3.connect")
    def test_create_logger(self, _):
        logger = DBLoggerAdapter(log_level=logging.INFO)
        assert logger is not None
        assert type(logger) == DBLoggerAdapter
        assert logger.log_level == logging.INFO
