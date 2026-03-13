from __future__ import annotations

import json
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from chatbot.bot import Chatbot
from chatbot.providers import ProviderConfig
from errors.handler import ConversationError, ProviderError

FAKE_PROVIDER = ProviderConfig(
    name="FakeProvider",
    base_url="https://fake.api/v1",
    api_key_env="FAKE_API_KEY",
    default_model="fake-model",
)


@pytest.fixture
def bot() -> Chatbot:
    with patch("chatbot.bot.OpenAI"):
        return Chatbot("fake-key", FAKE_PROVIDER)


class TestMessageManagement:
    def test_initial_messages_contain_system_prompt(self, bot: Chatbot) -> None:
        assert len(bot.messages) == 1
        assert bot.messages[0]["role"] == "system"

    def test_add_user_message(self, bot: Chatbot) -> None:
        bot.add_user_message("hello")
        assert bot.messages[-1] == {"role": "user", "content": "hello"}

    def test_add_assistant_message(self, bot: Chatbot) -> None:
        bot.add_assistant_message("hi there")
        assert bot.messages[-1] == {"role": "assistant", "content": "hi there"}

    def test_messages_accumulate_in_order(self, bot: Chatbot) -> None:
        bot.add_user_message("first")
        bot.add_assistant_message("second")
        bot.add_user_message("third")
        roles = [m["role"] for m in bot.messages]
        assert roles == ["system", "user", "assistant", "user"]


class TestGetReply:
    def test_successful_reply_adds_both_messages(self, bot: Chatbot) -> None:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "I'm a bot"
        bot._client.chat.completions.create.return_value = mock_response

        reply = bot.get_reply("hello")

        assert reply == "I'm a bot"
        assert len(bot.messages) == 3
        assert bot.messages[1] == {"role": "user", "content": "hello"}
        assert bot.messages[2] == {"role": "assistant", "content": "I'm a bot"}

    def test_none_reply_does_not_add_assistant_message(self, bot: Chatbot) -> None:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = None
        bot._client.chat.completions.create.return_value = mock_response

        reply = bot.get_reply("hello")

        assert reply is None
        assert len(bot.messages) == 2

    def test_api_error_raises_provider_error(self, bot: Chatbot) -> None:
        from openai import OpenAIError

        bot._client.chat.completions.create.side_effect = OpenAIError("boom")

        with pytest.raises(ProviderError, match="API request failed"):
            bot.get_reply("hello")


class TestTimestamp:
    def test_timestamp_format(self) -> None:
        ts = Chatbot.generate_timestamp()
        assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", ts)


class TestFilenameGeneration:
    def test_generates_filename_with_date(self) -> None:
        result = Chatbot.generate_filename_with_utc_date("history", "json")
        assert re.match(r"history_\d{8}\.json", result)

    def test_raises_on_empty_filename(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Chatbot.generate_filename_with_utc_date("", "json")

    def test_raises_on_empty_extension(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            Chatbot.generate_filename_with_utc_date("history", "")


class TestJsonFileOperations:
    def test_creates_new_file(self, tmp_path: Path) -> None:
        fp = str(tmp_path / "data.json")
        Chatbot.update_json_file(fp, {"key": "value"})

        with open(fp) as fh:
            data = json.load(fh)
        assert data == [{"key": "value"}]

    def test_appends_to_existing_file(self, tmp_path: Path) -> None:
        fp = str(tmp_path / "data.json")
        with open(fp, "w") as fh:
            json.dump([{"first": 1}], fh)

        Chatbot.update_json_file(fp, {"second": 2})

        with open(fp) as fh:
            data = json.load(fh)
        assert len(data) == 2
        assert data[1] == {"second": 2}

    def test_raises_on_invalid_json(self, tmp_path: Path) -> None:
        fp = str(tmp_path / "bad.json")
        with open(fp, "w") as fh:
            fh.write("not json")

        with pytest.raises(ConversationError, match="Invalid JSON"):
            Chatbot.update_json_file(fp, {"key": "value"})
