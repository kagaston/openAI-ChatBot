from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from chatbot.providers import PROVIDERS, ProviderConfig, resolve_api_key, resolve_provider


class TestProviderConfig:
    def test_openai_provider_exists(self) -> None:
        assert "openai" in PROVIDERS

    def test_xai_provider_exists(self) -> None:
        assert "xai" in PROVIDERS

    def test_openai_defaults(self) -> None:
        p = PROVIDERS["openai"]
        assert p.name == "OpenAI"
        assert p.base_url is None
        assert p.api_key_env == "OPENAI_API_KEY"
        assert p.default_model == "gpt-4o-mini"

    def test_xai_defaults(self) -> None:
        p = PROVIDERS["xai"]
        assert p.name == "xAI (Grok)"
        assert p.base_url == "https://api.x.ai/v1"
        assert p.api_key_env == "XAI_API_KEY"
        assert p.default_model == "grok-3-mini"

    def test_provider_config_is_frozen(self) -> None:
        p = PROVIDERS["openai"]
        with pytest.raises(AttributeError):
            p.name = "changed"  # type: ignore[misc]


class TestResolveProvider:
    @patch.dict(os.environ, {"CHATBOT_PROVIDER": "openai"}, clear=False)
    def test_resolves_openai_from_env(self) -> None:
        result = resolve_provider()
        assert result.name == "OpenAI"

    @patch.dict(os.environ, {"CHATBOT_PROVIDER": "xai"}, clear=False)
    def test_resolves_xai_from_env(self) -> None:
        result = resolve_provider()
        assert result.name == "xAI (Grok)"

    @patch.dict(os.environ, {"CHATBOT_PROVIDER": "XAI"}, clear=False)
    def test_resolves_case_insensitive(self) -> None:
        result = resolve_provider()
        assert result.name == "xAI (Grok)"

    @patch.dict(os.environ, {}, clear=True)
    def test_defaults_to_openai_when_unset(self) -> None:
        result = resolve_provider()
        assert result.name == "OpenAI"

    @patch.dict(os.environ, {"CHATBOT_PROVIDER": "bogus"}, clear=False)
    def test_raises_for_unknown_provider(self) -> None:
        with pytest.raises(ValueError, match="Unknown provider 'bogus'"):
            resolve_provider()


class TestResolveApiKey:
    @patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123"}, clear=False)
    def test_resolves_key_from_env(self) -> None:
        provider = PROVIDERS["openai"]
        assert resolve_api_key(provider) == "sk-test123"

    @patch.dict(os.environ, {"OPENAI_API_KEY": '"sk-quoted"'}, clear=False)
    def test_strips_surrounding_quotes(self) -> None:
        provider = PROVIDERS["openai"]
        assert resolve_api_key(provider) == "sk-quoted"

    @patch.dict(os.environ, {}, clear=True)
    def test_raises_when_key_missing(self) -> None:
        provider = PROVIDERS["openai"]
        with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
            resolve_api_key(provider)
