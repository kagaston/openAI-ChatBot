from __future__ import annotations

import os
from unittest.mock import patch

from settings.config import (
    CHATBOT_PROVIDER,
    LOG_FORMAT,
    LOG_LEVEL,
)


class TestDefaultValues:
    def test_chatbot_provider_default(self) -> None:
        assert isinstance(CHATBOT_PROVIDER, str)

    def test_log_format_default(self) -> None:
        assert LOG_FORMAT in ("color", "plain", "json")

    def test_log_level_default(self) -> None:
        assert LOG_LEVEL in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class TestEnvOverrides:
    @patch.dict(os.environ, {"CHATBOT_PROVIDER": "xai"}, clear=False)
    def test_provider_reads_from_env(self) -> None:
        import importlib

        import settings.config as cfg

        importlib.reload(cfg)
        assert cfg.CHATBOT_PROVIDER == "xai"

    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}, clear=False)
    def test_log_level_reads_from_env(self) -> None:
        import importlib

        import settings.config as cfg

        importlib.reload(cfg)
        assert cfg.LOG_LEVEL == "DEBUG"
