from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from chatbot.app import ChatbotApp
from chatbot.bot import Chatbot
from chatbot.providers import ProviderConfig

FAKE_PROVIDER = ProviderConfig(
    name="FakeProvider",
    base_url="https://fake.api/v1",
    api_key_env="FAKE_API_KEY",
    default_model="fake-model",
)


@patch("chatbot.bot.OpenAI")
def _make_app(_mock_openai: MagicMock) -> ChatbotApp:
    bot = Chatbot("fake-key", FAKE_PROVIDER)
    return ChatbotApp(bot, FAKE_PROVIDER.name)


class TestChatbotAppInit:
    def test_stores_chatbot_and_provider_name(self) -> None:
        app = _make_app()
        assert app.provider_name == "FakeProvider"
        assert isinstance(app.chatbot, Chatbot)


class TestHandleUserInput:
    def test_prints_reply_on_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        app = _make_app()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "bot reply"
        app.chatbot._client.chat.completions.create.return_value = mock_response

        app._handle_user_input("hello")

        captured = capsys.readouterr()
        assert "bot reply" in captured.out

    def test_prints_error_on_api_failure(self, capsys: pytest.CaptureFixture[str]) -> None:
        app = _make_app()
        from openai import OpenAIError

        app.chatbot._client.chat.completions.create.side_effect = OpenAIError("fail")

        app._handle_user_input("hello")

        captured = capsys.readouterr()
        assert captured.out  # error message printed

    def test_prints_fallback_when_reply_is_none(self, capsys: pytest.CaptureFixture[str]) -> None:
        app = _make_app()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = None
        app.chatbot._client.chat.completions.create.return_value = mock_response

        app._handle_user_input("hello")

        captured = capsys.readouterr()
        assert "Something went wrong" in captured.out


class TestSaveConversationHistory:
    def test_does_not_raise(self) -> None:
        app = _make_app()
        app._save_conversation_history()

    @patch("chatbot.app.Chatbot.update_json_file", side_effect=OSError("disk full"))
    def test_logs_and_swallows_exceptions(self, _mock_update: MagicMock) -> None:
        app = _make_app()
        app._save_conversation_history()
