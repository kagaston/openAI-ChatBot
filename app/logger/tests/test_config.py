from __future__ import annotations

import json
import logging
import os
from unittest.mock import patch

import pytest

import logger.config as lc
from logger.config import (
    ColorFormatter,
    JSONFormatter,
    PlainFormatter,
    get_logger,
    setup_logging,
)


@pytest.fixture(autouse=True)
def _reset_logging() -> None:
    """Reset the module-level _initialized flag between tests."""
    lc._initialized = False
    root = logging.getLogger()
    root.handlers.clear()


class TestColorFormatter:
    def test_formats_info_message(self) -> None:
        fmt = ColorFormatter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "hello", (), None)
        result = fmt.format(record)
        assert "hello" in result
        assert "INFO" in result

    def test_warning_colorizes_message(self) -> None:
        fmt = ColorFormatter()
        record = logging.LogRecord("test", logging.WARNING, "", 0, "warn!", (), None)
        result = fmt.format(record)
        assert "warn!" in result
        assert "\033[33m" in result


class TestPlainFormatter:
    def test_formats_without_ansi(self) -> None:
        fmt = PlainFormatter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "plain msg", (), None)
        result = fmt.format(record)
        assert "plain msg" in result
        assert "\033[" not in result


class TestJSONFormatter:
    def test_outputs_valid_json(self) -> None:
        fmt = JSONFormatter()
        record = logging.LogRecord("test.mod", logging.ERROR, "", 42, "boom", (), None)
        result = fmt.format(record)
        parsed = json.loads(result)
        assert parsed["level"] == "ERROR"
        assert parsed["msg"] == "boom"
        assert parsed["logger"] == "test.mod"
        assert "ts" in parsed

    def test_includes_exception_info(self) -> None:
        fmt = JSONFormatter()
        try:
            raise RuntimeError("kaboom")
        except RuntimeError:
            import sys

            exc_info = sys.exc_info()
        record = logging.LogRecord("test", logging.ERROR, "", 0, "err", (), exc_info)
        result = fmt.format(record)
        parsed = json.loads(result)
        assert "exception" in parsed
        assert "kaboom" in parsed["exception"]


class TestSetupLogging:
    @patch.dict(os.environ, {"LOG_FORMAT": "plain", "LOG_LEVEL": "WARNING"}, clear=False)
    def test_returns_named_logger(self) -> None:
        result = setup_logging("myapp")
        assert result.name == "myapp"

    @patch.dict(os.environ, {"LOG_FORMAT": "plain", "LOG_LEVEL": "DEBUG"}, clear=False)
    def test_sets_up_console_handler(self) -> None:
        setup_logging("myapp")
        root = logging.getLogger()
        assert len(root.handlers) >= 1


class TestGetLogger:
    def test_returns_namespaced_logger(self) -> None:
        log = get_logger("providers")
        assert log.name == "chatbot.providers"
