import os

from dotenv import load_dotenv


load_dotenv(override=True)


class Config:
    """
    Configuration class for LLMs, secret keys, and default values.
    Can be overridden by user setting Config.<attribute>.
    """

    # Llama LLMs
    LLAMA_API_KEY: str | None = os.environ.get("LLAMA_API_KEY")
    LLAMA_API_URL: str = os.environ.get("LLAMA_API_URL", "https://api.llama-api.com")
    DEFAULT_LLAMA_MODEL: str = "llama3-70b"

    # OpenAI LLMs
    OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_URL: str = os.environ.get("OPENAI_API_URL", "https://api.openai.com/v1")
    DEFAULT_OPENAI_MODEL: str = "gpt-4-1106-preview"

    # LLM parameters
    DEFAULT_TEMPERATURE: float = 0.0
