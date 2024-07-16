"""
==================================
LANGUAGE MODEL (LM) CONFIGURATIONS
==================================
"""


import os

from dotenv import load_dotenv


load_dotenv(override=True)


class LMConfig:
    """
    Configuration class for language models, secret keys, and default values.
    Can be overridden by user setting LMConfig.<attribute>.
    """

    # Llama LMs
    LLAMA_API_KEY: str | None = os.environ.get("LLAMA_API_KEY")
    LLAMA_API_URL: str = os.environ.get("LLAMA_API_URL", "https://api.llama-api.com")
    # DEFAULT_LLAMA_MODEL: str = "llama3-70b"
    DEFAULT_LLAMA_MODEL: str = "llama3-8b"

    # OpenAI LMs
    OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_URL: str = os.environ.get("OPENAI_API_URL", "https://api.openai.com/v1")
    DEFAULT_OPENAI_MODEL: str = "gpt-4-1106-preview"

    # HuggingFace LMs
    # HF_API_KEY: str | None = os.environ.get("HF_API_KEY")
    HF_API_KEY = "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"
    HF_API_URL: str = os.environ.get("HF_API_URL", "https://api-inference.huggingface.co/models/")
    # DEFAULT_LLAMA_MODEL: str = "llama3-70b"
    DEFAULT_HF_LLAMA_MODEL: str = "meta-llama/Meta-Llama-3-8B-Instruct"

    # LM parameters
    DEFAULT_SEED: int = 7 * 17 * 14717
    DEFAULT_TEMPERATURE: float = 0.0
