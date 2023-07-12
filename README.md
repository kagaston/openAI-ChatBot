# OpenAI ChatBot

This repository contains code and resources for building a chatbot using the OpenAI Chat API and the GPT-3.5-turbo model.

## Overview

The OpenAI ChatBot is an implementation that allows you to interact with a chatbot powered by the OpenAI GPT-3.5-turbo model. It provides a convenient way to add user messages, obtain chatbot replies, and save conversation history to a JSON file.

## Features

- Send user messages and receive chatbot replies using the OpenAI Chat API
- Maintain a conversation history with roles (user, assistant) and message content
- Save conversation history to a JSON file for reference or analysis
- Utilize utility methods for timestamp generation, JSON file updates, and filename generation

## Requirements

To use the OpenAI ChatBot, ensure you have the following:

- Python 3.x
- OpenAI API key

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/kagaston/openAI-ChatBot.git
   ```
   
2. Install the required dependencies:
    ```shell
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key:
Visit the OpenAI website to sign up for an API key.
Set the OPENAI_API_KEY environment variable or update the config.py file with your API key.
Explore the example code and files provided in the repository to understand how to use and customize the chatbot.

## Usage

To use the OpenAI ChatBot, follow these steps:

1. Import the Chatbot class from chatbot.py into your Python script.
2. Instantiate a Chatbot object by providing your OpenAI API key:
    ```python
    chatbot = Chatbot(api_key)
    ```
3. Add user messages to the conversation using the add_user_message(content) method.
4. Obtain chatbot replies based on user input using the get_reply(user_input) method.
5. Add assistant messages to the conversation using the add_assistant_message(content) method.
6. Save the conversation history to a JSON file using the save_to_file(file_path) method.
7. Refer to the code and comments in the repository for more detailed usage examples and customization options.

#Contributing

Contributions to the OpenAI ChatBot are welcome! If you encounter any issues or have suggestions for improvements, feel free to submit a pull request or open an issue on the repository.

#License

This project is licensed under the MIT License.