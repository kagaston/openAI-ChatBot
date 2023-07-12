import logging

from api_key_provider import APIKeyProvider, EnvironmentVariableProvider, DotEnvFileProvider
from colors import Color
from chatbot import Chatbot
from formatters import JSONFormatter


def configure_logging():
    """
    Configures the logging module to write logs to a file with a JSON formatter.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_file_name = "openAI-Chatbot-log.json"
    formatter = JSONFormatter()
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


class ChatbotApp:
    """
    Chatbot application class that encapsulates the chatbot interaction loop.

    Attributes:
        chatbot (Chatbot): The instance of the Chatbot class.
        logger (logging.Logger): The logger instance for logging.

    Methods:
        run(): Runs the chatbot interaction loop.
        handle_user_input(user_input): Handles user input and generates a chatbot reply.
        save_conversation_history(): Saves the conversation history to a file.
    """

    def __init__(self, api_key):
        """
        Initializes the ChatbotApp instance with the provided API key.

        Args:
            api_key (str): The API key for accessing the OpenAI Chat API.
        """
        self.chatbot = Chatbot(api_key)
        self.logger = configure_logging()

    def run(self):
        """
        Runs the chatbot interaction loop.

        The loop continues until the user enters "exit" or "quit".
        """
        while True:
            user_input = input(Color.GREEN.value + "User: " + Color.END.value)
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Chatbot: Goodbye!")
                break

            self.handle_user_input(user_input)
            self.save_conversation_history()

    def handle_user_input(self, user_input):
        """
        Handles user input and generates a chatbot reply.

        Args:
            user_input (str): The user's input message.
        """
        self.chatbot.add_user_message(user_input)
        reply = self.chatbot.get_reply(user_input)
        if reply:
            self.chatbot.add_assistant_message(reply)
            print(Color.GREEN.value + "Chatbot: " + Color.END.value + Color.BLUE.value + reply + Color.END.value)
        else:
            print(Color.RED.value + "Oops! Something went wrong. Please try again." + Color.END.value)

    def save_conversation_history(self):
        """
        Saves the conversation history to a file.
        """
        try:
            chat_data = {
                "ts": self.chatbot.generate_timestamp(),
                "messages": self.chatbot.messages
            }
            file_path = self.chatbot.generate_filename_with_utc_date("conversation_history", "json")
            self.chatbot.update_json_file(file_path, chat_data)
        except Exception as e:
            self.logger.exception(f"An error occurred while saving conversation history: {str(e)}")


def main():
    """
    Main function to run the chatbot application.

    - Loads the API key from the environment variable.
    - Instantiates the ChatbotApp.
    - Runs the chatbot interaction loop.
    """
    api_key_name = "OPENAI_API_KEY"
    api_key_provider = APIKeyProvider(api_key_name)
    api_key = api_key_provider.get_api_key()

    chatbot_app = ChatbotApp(api_key)
    chatbot_app.run()


if __name__ == '__main__':
    main()
