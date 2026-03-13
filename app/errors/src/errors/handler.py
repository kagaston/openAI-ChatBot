"""Custom exception hierarchy and global error handler for openAI-ChatBot."""

from __future__ import annotations

from logger.config import get_logger

log = get_logger("error_handler")


class ChatbotError(Exception):
    """Base exception for openAI-ChatBot."""

    def __init__(self, message: str, *, provider: str | None = None) -> None:
        super().__init__(message)
        self.provider = provider


class ProviderError(ChatbotError):
    """Raised when API communication with a provider fails."""


class ConfigError(ChatbotError):
    """Raised when configuration or environment setup is invalid."""


class ConversationError(ChatbotError):
    """Raised when conversation history operations fail."""


def handle_error(exc: Exception, *, context: str | None = None) -> str:
    """Log the error and return a user-friendly message."""
    if isinstance(exc, ConfigError):
        log.error("Config error: %s", exc)
        return f"Configuration problem: {exc}"

    if isinstance(exc, ProviderError):
        log.error("Provider error: %s (provider=%s)", exc, getattr(exc, "provider", None))
        return f"Provider error: {exc}"

    if isinstance(exc, ConversationError):
        log.error("Conversation error: %s", exc)
        return f"Conversation error: {exc}"

    log.exception("Unexpected error in context=%s", context)
    return "An unexpected error occurred. Check logs for details."
