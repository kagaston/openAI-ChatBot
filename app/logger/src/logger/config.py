"""Shared logging configuration for openAI-ChatBot.

ANSI color output on TTY, plain text to rotating log files, structured JSON
for production environments.

Usage -- startup::

    from logger.config import setup_logging
    setup_logging("chatbot", verbose=True)

Usage -- library modules::

    from logger.config import get_logger
    log = get_logger("providers")
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"

_LEVEL_COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[41m",
}

_NAME_COLOR = "\033[34m"
_FUNC_COLOR = "\033[35m"
_TIME_COLOR = "\033[90m"

_PLAIN_FMT = "%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


class ColorFormatter(logging.Formatter):
    """ANSI-colored console output for development."""

    def __init__(self) -> None:
        super().__init__(_PLAIN_FMT, datefmt=_DATE_FMT)

    def format(self, record: logging.LogRecord) -> str:
        level_color = _LEVEL_COLORS.get(record.levelname, "")
        level_tag = f"{level_color}{_BOLD}{record.levelname:<8}{_RESET}"
        name_tag = f"{_NAME_COLOR}{record.name}{_RESET}"
        func_tag = f"{_FUNC_COLOR}{record.funcName}:{record.lineno}{_RESET}"
        time_tag = f"{_TIME_COLOR}{self.formatTime(record, self.datefmt)}{_RESET}"
        msg = record.getMessage()

        if record.levelno >= logging.WARNING:
            msg = f"{level_color}{msg}{_RESET}"

        formatted = f"{time_tag} | {level_tag} | {name_tag}.{func_tag} | {msg}"

        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted += f"\n{_DIM}{record.exc_text}{_RESET}"
        if record.stack_info:
            formatted += f"\n{_DIM}{record.stack_info}{_RESET}"

        return formatted


class PlainFormatter(logging.Formatter):
    """Plain-text formatter for log files."""

    def __init__(self) -> None:
        super().__init__(_PLAIN_FMT, datefmt=_DATE_FMT)


class JSONFormatter(logging.Formatter):
    """Structured JSON log output for production environments."""

    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "func": f"{record.funcName}:{record.lineno}",
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0] is not None:
            entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(entry)


_CONSOLE_HANDLER_NAME = "_chatbot_console"
_initialized = False


def _find_log_dir() -> Path | None:
    current = Path.cwd().resolve()
    for _ in range(20):
        if (current / "logs").is_dir():
            return current / "logs"
        if (current / ".env").is_file() or (current / "justfile").is_file():
            log_dir = current / "logs"
            log_dir.mkdir(exist_ok=True)
            return log_dir
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def setup_logging(
    app_name: str = "chatbot",
    *,
    verbose: bool = False,
    log_dir: Path | str | None = None,
    console: bool = True,
    color: bool = True,
    max_bytes: int = 10_485_760,
    backup_count: int = 5,
) -> logging.Logger:
    """Configure logging for the application. Call once at startup."""
    global _initialized  # noqa: PLW0603
    root = logging.getLogger()

    log_format = os.getenv("LOG_FORMAT", "color")
    log_level_str = os.getenv("LOG_LEVEL", "DEBUG" if verbose else "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    if not _initialized:
        root.setLevel(logging.DEBUG)
        root.handlers.clear()

        if console:
            ch = logging.StreamHandler(sys.stderr)
            ch.setLevel(logging.DEBUG if verbose else log_level)

            if log_format == "json":
                ch.setFormatter(JSONFormatter())
            else:
                use_color = (
                    color and log_format != "plain" and hasattr(sys.stderr, "isatty") and sys.stderr.isatty()
                )
                ch.setFormatter(ColorFormatter() if use_color else PlainFormatter())

            ch.set_name(_CONSOLE_HANDLER_NAME)
            root.addHandler(ch)

        resolved_dir = Path(log_dir) if log_dir is not None else _find_log_dir()
        if resolved_dir is not None:
            resolved_dir.mkdir(parents=True, exist_ok=True)
            fh = RotatingFileHandler(
                resolved_dir / f"{app_name}.log",
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(PlainFormatter())
            root.addHandler(fh)

        for noisy in ("urllib3", "httpx", "httpcore", "openai"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

        _initialized = True
    elif verbose:
        for h in root.handlers:
            if getattr(h, "name", None) == _CONSOLE_HANDLER_NAME:
                h.setLevel(logging.DEBUG)

    return logging.getLogger(app_name)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for a module. Safe to call at module level."""
    return logging.getLogger(f"chatbot.{name}")
