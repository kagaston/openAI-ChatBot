from __future__ import annotations

import pytest

from errors.handler import (
    ChatbotError,
    ConfigError,
    ConversationError,
    ProviderError,
    handle_error,
)


class TestExceptionHierarchy:
    def test_provider_error_is_chatbot_error(self) -> None:
        assert issubclass(ProviderError, ChatbotError)

    def test_config_error_is_chatbot_error(self) -> None:
        assert issubclass(ConfigError, ChatbotError)

    def test_conversation_error_is_chatbot_error(self) -> None:
        assert issubclass(ConversationError, ChatbotError)

    def test_chatbot_error_stores_provider(self) -> None:
        exc = ChatbotError("fail", provider="OpenAI")
        assert exc.provider == "OpenAI"
        assert str(exc) == "fail"

    def test_chatbot_error_provider_defaults_to_none(self) -> None:
        exc = ChatbotError("fail")
        assert exc.provider is None


class TestHandleError:
    def test_handles_config_error(self) -> None:
        msg = handle_error(ConfigError("bad config"))
        assert "Configuration problem" in msg

    def test_handles_provider_error(self) -> None:
        msg = handle_error(ProviderError("timeout", provider="xAI"))
        assert "Provider error" in msg

    def test_handles_conversation_error(self) -> None:
        msg = handle_error(ConversationError("corrupt file"))
        assert "Conversation error" in msg

    def test_handles_unexpected_error(self) -> None:
        msg = handle_error(RuntimeError("surprise"))
        assert "unexpected error" in msg.lower()

    def test_passes_context_for_unknown_errors(self) -> None:
        msg = handle_error(RuntimeError("oops"), context="save_history")
        assert "unexpected error" in msg.lower()
