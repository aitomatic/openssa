"""
==================================
LANGUAGE MODEL (LM) CONFIGURATIONS
==================================
"""


import os

from dotenv import load_dotenv


load_dotenv(dotenv_path='.env', override=True)


class LMConfig:
    """
    Configuration class for language models, secret keys, and default values.
    Can be overridden by user setting LMConfig.<attribute>.
    """

    # HuggingFace LMs
    HF_API_KEY: str | None = os.environ.get('HF_API_KEY')
    HF_API_URL: str = os.environ.get('HF_API_URL', 'https://api-inference.huggingface.co/models')
    HF_DEFAULT_MODEL: str = 'meta-llama/Meta-Llama-3.1-70B-Instruct'
    HF_DEFAULT_SMALL_MODEL: str = 'meta-llama/Meta-Llama-3.1-8B-Instruct'

    # Llama LMs
    LLAMA_API_KEY: str | None = os.environ.get('LLAMA_API_KEY')
    LLAMA_API_URL: str = os.environ.get('LLAMA_API_URL', '...')
    LLAMA_DEFAULT_MODEL: str = 'llama3-70b'
    LLAMA_DEFAULT_SMALL_MODEL: str = 'llama3-8b'

    # OpenAI LMs
    OPENAI_API_KEY: str | None = os.environ.get('OPENAI_API_KEY')
    OPENAI_API_URL: str = os.environ.get('OPENAI_API_URL', 'https://api.openai.com/v1')
    OPENAI_DEFAULT_MODEL: str = 'gpt-4o'  # platform.openai.com/docs/models/gpt-4o
    OPENAI_DEFAULT_SMALL_MODEL: str = 'gpt-4o-mini'  # platform.openai.com/docs/models/gpt-4o-mini

    # OLLAMA LMs
    OLLAMA_DEFAULT_MODEL: str = os.environ.get('OLLAMA_MODEL', 'llama3.1:70b')
    OLLAMA_API_URL: str = os.environ.get('OLLAMA_API_URL', 'http://localhost:11434')
    OLLAMA_DEFAULT_EMBEDDING_MODEL: str = os.environ.get('OLLAMA_EMBEDDING_MODEL', 'mxbai-embed-large')
    OLLAMA_DEFAULT_TIMEOUT: int = os.environ.get('OLLAMA_TIMEOUT', 600)
    OLLAMA_DEFAULT_TEMPERATURE: float = 0.1

    # LM parameters
    DEFAULT_SEED: int = 7 * 17 * 14717
    DEFAULT_TEMPERATURE: float = 0.0
