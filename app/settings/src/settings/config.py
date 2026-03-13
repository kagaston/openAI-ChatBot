"""System-wide configuration constants and environment defaults."""

import os

# --- Provider Selection ---
CHATBOT_PROVIDER = os.getenv("CHATBOT_PROVIDER", "openai")

# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- xAI (Grok) ---
XAI_API_KEY = os.getenv("XAI_API_KEY", "")

# --- Logging ---
LOG_FORMAT = os.getenv("LOG_FORMAT", "color")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
