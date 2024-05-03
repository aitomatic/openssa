from __future__ import annotations
import os
from typing import Optional
import dotenv

dotenv.load_dotenv(override=True)

class Config:
    """
    Configuration class for LLMs, secret keys, and default values.
    Can be overridden by user setting Config.<attribute>.
    """
    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_LLAMA_MODEL = "llama3-70b"
    DEFAULT_OPENAI_MODEL = "gpt-4-1106-preview"

    LLAMA_API_KEY: Optional[str] = os.environ.get("LLAMA_API_KEY")
    LLAMA_API_URL: Optional[str] = (
        os.environ.get("LLAMA_API_URL") or "https://api.llama-api.com"
    )

    OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_URL: Optional[str] = (
        os.environ.get("OPENAI_API_URL") or "https://api.openai.com/v1"
    )
