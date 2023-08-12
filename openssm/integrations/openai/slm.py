import os
from abc import ABC
from typing import Optional
from pydantic import BaseModel
import openai
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.slm.base_slm import BaseSLM
from openssm.utils.config import Config
from openssm.utils.logs import Logs


Config.OPENAI_API_KEY: Optional[str] = os.environ.get('OPENAI_API_KEY')
Config.OPENAI_API_URL: Optional[str] = os.environ.get('OPENAI_API_URL') or "https://api.openai.com/v1"
Config.AZURE_GPT4_API_KEY: Optional[str] = os.environ.get('AZURE_GPT4_API_KEY')
Config.AZURE_GPT4_API_URL: Optional[str] = os.environ.get('AZURE_GPT4_API_URL')
Config.AZURE_GPT4_ENGINE: Optional[str] = os.environ.get('AZURE_GPT4_ENGINE')


class APIContext(BaseModel):
    type: Optional[str] = "openai"
    key: Optional[str] = None
    base: Optional[str] = None
    version: Optional[str] = "v1"
    type: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo"
    engine: Optional[str] = None
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7
    is_chat_completion: Optional[bool] = True

    @classmethod
    def from_defaults(cls):
        api_context = APIContext()
        api_context.key = Config.OPENAI_API_KEY
        api_context.base = Config.OPENAI_API_URL
        return api_context


class _AbstractSLM(BaseSLM, ABC):

    def __init__(self, api_context: APIContext = APIContext(), adapter: AbstractAdapter = None):
        api_context.key = api_context.key or Config.OPENAI_API_KEY
        api_context.base = api_context.base or Config.OPENAI_API_URL

        if api_context.key is None:
            raise ValueError("api_key must be provided, e.g., via Config.OPENAI_API_KEY or 'sk-xxxxx'")

        if api_context.model is None and api_context.engine is None:
            raise ValueError("model or engine must be provided (e.g., 'gpt-3.5-turbo'))")

        super().__init__(adapter)

        self._api_context = api_context

    @property
    def api_context(self) -> APIContext:
        if self._api_context is None:
            self._api_context = APIContext()
        return self._api_context


class SLM(_AbstractSLM):
    def __init__(self, api_context: APIContext = APIContext(), adapter: AbstractAdapter = None):
        """
        :param api_context: APIContext object with the API key, base URL, model, engine, etc.
        :param adapter: Adapter object to use for the SLM.
        """
        super().__init__(api_context, adapter)

    def _call_lm_api(self, conversation: list[dict]) -> dict:
        # pylint: disable=unused-argument
        if self.api_context.is_chat_completion:
            return self._call_chat_completion_api(conversation)

        return self._call_completion_api(conversation)

    @Logs.do_log_entry_and_exit()
    def _call_completion_api(self, conversation: list[dict]) -> dict:
        prompt = self._make_completion_prompt(conversation)

        response = openai.Completion.create(
            prompt=prompt,
            api_type=self.api_context.type,
            api_key=self.api_context.key,
            api_base=self.api_context.base,
            api_version=self.api_context.version,
            model=self.api_context.model,
            engine=self.api_context.engine,
            max_tokens=self.api_context.max_tokens,
            temperature=self.api_context.temperature
        )
        response = response.choices[0].text.strip()

        reply = self._parse_llm_response(response)
        if isinstance(reply, list):
            if len(reply) == 0 or len(reply[0]) == 0:
                reply = {'role': 'assistant', 'content': 'I got nothing.'}

        return reply

    @Logs.do_log_entry_and_exit()
    def _call_chat_completion_api(self, conversation: list[dict]) -> dict:
        response = openai.ChatCompletion.create(
            messages=conversation,
            api_type=self.api_context.type,
            api_key=self.api_context.key,
            api_base=self.api_context.base,
            api_version=self.api_context.version,
            # model=self.api_context.model,
            engine=self.api_context.engine,
            max_tokens=self.api_context.max_tokens,
            temperature=self.api_context.temperature
        )

        response = response.choices[0].message

        return response


class GPT3ChatCompletionSLM(SLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.is_chat_completion = True
        api_context.model = "gpt-3.5-turbo"
        api_context.engine = None
        super().__init__(api_context, adapter=adapter)


class GPT3CompletionSLM(SLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.is_chat_completion = False
        api_context.model = "text-davinci-002"
        api_context.engine = None
        super().__init__(api_context, adapter=adapter)


class GPT4ChatCompletionSLM(SLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()
            api_context.type = "azure"
            api_context.key = Config.AZURE_GPT4_API_KEY
            api_context.base = Config.AZURE_GPT4_API_URL
            api_context.engine = Config.AZURE_GPT4_ENGINE

        api_context.is_chat_completion = True
        api_context.model = None
        api_context.version = "2023-03-15-preview"
        super().__init__(api_context, adapter=adapter)
