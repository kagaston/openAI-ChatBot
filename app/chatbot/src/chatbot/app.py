"""CLI application that drives the chatbot REPL."""

from __future__ import annotations

from chatbot.bot import Chatbot
from chatbot.colors import Color
from chatbot.providers import resolve_api_key, resolve_provider
from errors import handle_error
from logger import get_logger, setup_logging

log = get_logger("app")


class ChatbotApp:
    """CLI wrapper around :class:`Chatbot`."""

    def __init__(self, chatbot: Chatbot, provider_name: str) -> None:
        self.chatbot = chatbot
        self.provider_name = provider_name

    def run(self) -> None:
        print(f"{Color.CYAN.value}Using provider: {self.provider_name}{Color.END.value}")
        while True:
            user_input = input(f"{Color.GREEN.value}User: {Color.END.value}")
            if user_input.lower() in ("exit", "quit", "q"):
                print("Chatbot: Goodbye!")
                break

            self._handle_user_input(user_input)
            self._save_conversation_history()

    def _handle_user_input(self, user_input: str) -> None:
        try:
            reply = self.chatbot.get_reply(user_input)
        except Exception as exc:
            msg = handle_error(exc, context="handle_user_input")
            print(f"{Color.RED.value}{msg}{Color.END.value}")
            return

        if reply:
            print(
                f"{Color.GREEN.value}Chatbot: {Color.END.value}"
                f"{Color.BLUE.value}{reply}{Color.END.value}"
            )
        else:
            print(f"{Color.RED.value}Oops! Something went wrong. Please try again.{Color.END.value}")

    def _save_conversation_history(self) -> None:
        try:
            chat_data = {
                "ts": self.chatbot.generate_timestamp(),
                "messages": self.chatbot.messages,
            }
            file_path = self.chatbot.generate_filename_with_utc_date("conversation_history", "json")
            self.chatbot.update_json_file(file_path, chat_data)
        except Exception as exc:
            log.exception("Failed to save conversation history: %s", exc)


def main() -> None:
    setup_logging("chatbot")
    provider = resolve_provider()
    api_key = resolve_api_key(provider)
    chatbot = Chatbot(api_key, provider)
    ChatbotApp(chatbot, provider.name).run()
