"""Core chatbot backed by an OpenAI-compatible Chat Completions API."""

from __future__ import annotations

from datetime import datetime, timezone
from json import JSONDecodeError, dump, load
from os import path
from typing import cast

from openai import OpenAI, OpenAIError
from openai.types.chat import ChatCompletionMessageParam

from chatbot.providers import ProviderConfig
from errors.handler import ConversationError, ProviderError


class Chatbot:
    """Interactive chatbot backed by an OpenAI-compatible Chat Completions API."""

    def __init__(self, api_key: str, provider: ProviderConfig) -> None:
        self._client: OpenAI = OpenAI(api_key=api_key, base_url=provider.base_url)
        self._model: str = provider.default_model
        self._provider: ProviderConfig = provider
        self.messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def get_reply(self, user_input: str) -> str | None:
        """Send *user_input*, get a reply, and record both in history."""
        self.add_user_message(user_input)
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=self.messages,
            )
            reply = response.choices[0].message.content
        except OpenAIError as exc:
            raise ProviderError(f"API request failed: {exc}", provider=self._provider.name) from exc

        if reply:
            self.add_assistant_message(reply)
        return reply

    def save_to_file(self) -> None:
        chat_data: dict[str, object] = {"ts": self.generate_timestamp(), "messages": self.messages}
        file_path = self.generate_filename_with_utc_date("conversation_history", "json")
        self.update_json_file(file_path, chat_data)

    @staticmethod
    def generate_timestamp() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def update_json_file(file_path: str, new_data: dict[str, object]) -> None:
        try:
            existing_data: list[dict[str, object]]
            if path.exists(file_path):
                with open(file_path, "r") as fh:
                    existing_data = cast(list[dict[str, object]], load(fh))
            else:
                existing_data = []

            existing_data.append(new_data)

            with open(file_path, "w") as fh:
                dump(existing_data, fh, indent=4)
        except JSONDecodeError as exc:
            raise ConversationError("Invalid JSON file!") from exc

    @staticmethod
    def generate_filename_with_utc_date(file_name: str, extension: str) -> str:
        if not file_name or not extension:
            raise ValueError("Both file_name and extension must be non-empty strings.")

        formatted_date = datetime.now(timezone.utc).strftime("%Y%m%d")
        return f"{file_name}_{formatted_date}.{extension}"
