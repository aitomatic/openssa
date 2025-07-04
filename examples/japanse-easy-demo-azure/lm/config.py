import os


class LMConfig:
    """
    Configuration class for language models, secret keys, and default values.
    Can be overridden by user setting LMConfig.<attribute>.
    """

    # Azure OpenAI LMs
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_GPT_MODEL_NAME = os.environ.get('AZURE_OPENAI_GPT_MODEL_NAME')
    AZURE_OPENAI_GPT_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME')

    # LM parameters
    DEFAULT_SEED: int = 7 * 17 * 14717
    DEFAULT_TEMPERATURE: float = 0.0
