import os
from typing import Optional
from openssa.utils.config import Config
from openssa.core.ssm.base_ssm import BaseSSM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.integrations.openai.ssm import SLM as OpenAISLM
from openssa.integrations.api_context import AbstractAPIContext


Config.AZURE_GPT3_API_VERSION: Optional[str] = os.environ.get('AZURE_GPT3_API_VERSION') or "2023-07-01-preview"
Config.AZURE_GPT3_API_URL: Optional[str] = os.environ.get('AZURE_GPT3_API_URL')
Config.AZURE_GPT3_API_KEY: Optional[str] = os.environ.get('AZURE_GPT3_API_KEY')
Config.AZURE_GPT3_ENGINE: Optional[str] = os.environ.get('AZURE_GPT3_ENGINE')
Config.AZURE_GPT3_MODEL: Optional[str] = os.environ.get('AZURE_GPT3_MODEL')

Config.AZURE_GPT4_API_VERSION: Optional[str] = os.environ.get('AZURE_GPT4_API_VERSION') or "2023-03-15-preview"
Config.AZURE_GPT4_API_URL: Optional[str] = os.environ.get('AZURE_GPT4_API_URL')
Config.AZURE_GPT4_API_KEY: Optional[str] = os.environ.get('AZURE_GPT4_API_KEY')
Config.AZURE_GPT4_ENGINE: Optional[str] = os.environ.get('AZURE_GPT4_ENGINE')
Config.AZURE_GPT4_MODEL: Optional[str] = os.environ.get('AZURE_GPT4_MODEL')


# pylint: disable=too-many-instance-attributes
class APIContext(AbstractAPIContext):
    @classmethod
    def from_defaults(cls):
        return APIContext.gpt3_defaults()

    @classmethod
    def gpt3_defaults(cls):
        api_context = APIContext()
        api_context.type = "azure"
        api_context.version = Config.AZURE_GPT3_API_VERSION
        api_context.base = Config.AZURE_GPT3_API_URL
        api_context.key = Config.AZURE_GPT3_API_KEY
        api_context.engine = Config.AZURE_GPT3_ENGINE
        api_context.model = Config.AZURE_GPT3_MODEL
        api_context.max_tokens = 2000
        api_context.temperature = 0.7
        api_context.is_chat_completion = True
        return api_context

    @classmethod
    def gpt4_defaults(cls):
        api_context = APIContext()
        api_context.type = "azure"
        api_context.version = Config.AZURE_GPT4_API_VERSION
        api_context.base = Config.AZURE_GPT4_API_URL
        api_context.key = Config.AZURE_GPT4_API_KEY
        api_context.engine = Config.AZURE_GPT4_ENGINE
        api_context.model = Config.AZURE_GPT4_MODEL
        api_context.max_tokens = 2000
        api_context.temperature = 0.7
        api_context.is_chat_completion = True
        return api_context


class GPT3ChatCompletionSLM(OpenAISLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.gpt3_defaults()

        api_context.is_chat_completion = True

        super().__init__(api_context, adapter=adapter)


class GPT3ChatCompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT3ChatCompletionSLM(), adapter, backends)


class GPT3CompletionSLM(OpenAISLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.is_chat_completion = False

        super().__init__(api_context, adapter=adapter)


class GPT3CompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT3CompletionSLM(), adapter, backends)


class GPT4ChatCompletionSLM(OpenAISLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.gpt4_defaults()

        api_context.is_chat_completion = True

        super().__init__(api_context, adapter=adapter)


class GPT4ChatCompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT4ChatCompletionSLM(), adapter, backends)
