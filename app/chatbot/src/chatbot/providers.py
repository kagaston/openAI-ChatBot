"""Provider registry for OpenAI-compatible chat APIs."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_PROVIDER = "openai"


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str | None
    api_key_env: str
    default_model: str


PROVIDERS: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="OpenAI",
        base_url=None,
        api_key_env="OPENAI_API_KEY",
        default_model="gpt-4o-mini",
    ),
    "xai": ProviderConfig(
        name="xAI (Grok)",
        base_url="https://api.x.ai/v1",
        api_key_env="XAI_API_KEY",
        default_model="grok-3-mini",
    ),
}


def resolve_provider() -> ProviderConfig:
    """Read CHATBOT_PROVIDER from the environment and return its config."""
    load_dotenv()
    name = os.environ.get("CHATBOT_PROVIDER", DEFAULT_PROVIDER).lower()
    if name not in PROVIDERS:
        available = ", ".join(sorted(PROVIDERS))
        raise ValueError(f"Unknown provider '{name}'. Available providers: {available}")
    return PROVIDERS[name]


def resolve_api_key(provider: ProviderConfig) -> str:
    """Resolve the API key for a given provider from the environment."""
    load_dotenv()
    api_key = os.environ.get(provider.api_key_env)
    if not api_key:
        raise ValueError(f"{provider.api_key_env} not found in environment variables or .env file")
    return api_key.strip('"')
