import os
from typing import Optional
from openssm.integrations.openai.slm import SLM as OpenAISLM, APIContext
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.utils.config import Config


Config.LEPTONAI_API_KEY: Optional[str] = os.environ.get('LEPTONAI_API_KEY') or None
Config.LEPTONAI_API_URL: Optional[str] = os.environ.get('LEPTONAI_API_URL') or None


class SLM(OpenAISLM):
    def __init__(self, api_context: APIContext = APIContext(), adapter: AbstractAdapter = None):
        api_context.key = Config.LEPTONAI_API_KEY
        api_context.base = Config.LEPTONAI_API_URL
        api_context.model = "gpt-3.5-turbo"
        super().__init__(api_context, adapter)
