# OpenAI ChatBot

A CLI chatbot supporting OpenAI-compatible Chat Completions APIs.

| Provider | Default Model | Docs |
|----------|--------------|------|
| **OpenAI** | `gpt-4o-mini` | [platform.openai.com](https://platform.openai.com/docs) |
| **xAI (Grok)** | `grok-3-mini` | [docs.x.ai](https://docs.x.ai/overview) |

## Project Structure

```
openAI-ChatBot/
├── app/
│   ├── chatbot/          # Main CLI application
│   │   ├── src/chatbot/
│   │   └── tests/
│   ├── logger/           # Shared logging (color, plain, JSON)
│   │   ├── src/logger/
│   │   └── tests/
│   ├── settings/         # Environment config constants
│   │   ├── src/settings/
│   │   └── tests/
│   └── errors/           # Exception hierarchy and error handler
│       ├── src/errors/
│       └── tests/
├── justfile
├── pyproject.toml
└── .env.example
```

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- An API key from at least one supported provider

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/kagaston/openAI-ChatBot.git
   cd openAI-ChatBot
   ```

2. Install dependencies:

   ```shell
   just install
   ```

3. Copy and fill in your `.env`:

   ```shell
   cp .env.example .env
   ```

   ```shell
   # OpenAI (default)
   CHATBOT_PROVIDER=openai
   OPENAI_API_KEY=sk-...

   # -- or xAI (Grok) --
   CHATBOT_PROVIDER=xai
   XAI_API_KEY=xai-...
   ```

4. Run the chatbot:

   ```shell
   just run
   ```

   Type `exit`, `quit`, or `q` to end the session.

## Development

```shell
just install        # install deps
just format         # ruff format
just lint           # ruff check --fix
just typecheck      # basedpyright
just test           # all tests
just test chatbot   # tests for one package
just update         # uv lock --upgrade
just clean          # remove caches
```

## Adding a New Provider

Add an entry in `app/chatbot/src/chatbot/providers.py`:

```python
PROVIDERS["my_provider"] = ProviderConfig(
    name="My Provider",
    base_url="https://api.example.com/v1",
    api_key_env="MY_PROVIDER_API_KEY",
    default_model="my-model",
)
```

Then set `CHATBOT_PROVIDER=my_provider` and the corresponding API key in `.env`.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
