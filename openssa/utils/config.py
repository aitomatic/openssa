import os
import dotenv
from openssa.utils.logs import mlogger
from typing import Optional


dotenv.load_dotenv(override=True)
mlogger.debug("Loaded environment variables from .env file")


class Config:
    """
    This class is used to store config setings, as well as
    secrets, such as API keys, tokens, etc.
    By default, they come from documented environment variables.
    But the user can override them by setting them directly
    in the Config object.
    """

    _dummy = "value is not set"

    DEBUG = False

    DEFAULT_TEMPERATURE = 0.0

    AITOMATIC_API_KEY: Optional[str] = os.environ.get("AITOMATIC_API_KEY")
    AITOMATIC_API_URL: Optional[str] = (
        os.environ.get("AITOMATIC_API_URL")
        or "https://aimo-api-mvp.platform.aitomatic.com/api/v1"
    )

    AITOMATIC_API_URL_7B: Optional[str] = os.environ.get("AITOMATIC_API_URL_7B")
    AITOMATIC_API_URL_70B: Optional[str] = os.environ.get("AITOMATIC_API_URL_70B")

    OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
    OPENAI_API_URL: Optional[str] = (
        os.environ.get("OPENAI_API_URL") or "https://api.openai.com/v1"
    )

    AZURE_API_VERSION: Optional[str] = (
        os.environ.get("AZURE_API_VERSION") or "2024-02-15-preview"
    )
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation#latest-preview-api-release

    AZURE_OPENAI_API_KEY: Optional[str] = os.environ.get("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_URL: Optional[str] = (
        os.environ.get("AZURE_OPENAI_API_URL") or "https://aiva-japan.openai.azure.com"
    )

    US_AZURE_OPENAI_API_KEY: Optional[str] = os.environ.get("US_AZURE_OPENAI_API_KEY")
    US_AZURE_OPENAI_API_BASE: Optional[str] = (
        os.environ.get("US_AZURE_OPENAI_API_BASE")
        or "https://aiva-dev.openai.azure.com/"
    )

    LEPTON_API_KEY: Optional[str] = os.environ.get("LEPTON_API_KEY")
    LEPTON_API_URL: Optional[str] = (
        os.environ.get("LEPTON_API_URL") or "https://llama2-7b.lepton.run/api/v1"
    )

    @staticmethod
    def setenv(var_name):
        """
        Copy the value of a config variable to an environment variable.
        If the variable is not set, nothing is changed.
        """
        value = getattr(Config, var_name, None)
        if value is not None:
            os.environ[var_name] = value
