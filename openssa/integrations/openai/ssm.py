import os
from abc import ABC
from typing import Optional
from openai import OpenAI

from openssa.utils.config import Config
from openssa.core.ssm.base_ssm import BaseSSM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.core.slm.base_slm import BaseSLM
from openssa.utils.logs import Logs
from openssa.integrations.api_context import AbstractAPIContext


Config.OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
Config.OPENAI_API_URL: Optional[str] = (
    os.environ.get("OPENAI_API_URL") or "https://api.openai.com/v1"
)



# pylint: disable=too-many-instance-attributes
class APIContext(AbstractAPIContext):
    @classmethod
    def from_defaults(cls):
        return APIContext.gpt3_defaults()

    @classmethod
    def gpt3_defaults(cls):
        api_context = APIContext()
        api_context.type = "openai"
        api_context.key = Config.OPENAI_API_KEY
        api_context.base = Config.OPENAI_API_URL
        api_context.model = "gpt-3.5-turbo"
        api_context.version = "v1"
        api_context.max_tokens = 2000
        api_context.temperature = 0.7
        api_context.is_chat_completion = True
        return api_context

    @classmethod
    def gpt4_defaults(cls):
        raise NotImplementedError("GPT-4 is not yet supported by OpenAI.")


class _AbstractSLM(BaseSLM, ABC):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.key = api_context.key or Config.OPENAI_API_KEY
        api_context.base = api_context.base or Config.OPENAI_API_URL

        if api_context.key is None:
            raise ValueError(
                "api_key must be provided, e.g., via Config.OPENAI_API_KEY or 'sk-xxxxx'"
            )

        if api_context.model is None and api_context.engine is None:
            raise ValueError(
                "model or engine must be provided (e.g., 'gpt-3.5-turbo'))"
            )

        super().__init__(adapter)

        self._api_context = api_context

        self.client = OpenAI()

    @property
    def api_context(self) -> APIContext:
        if self._api_context is None:
            self._api_context = APIContext
        return self._api_context


class SLM(_AbstractSLM):
    def _call_lm_api(self, conversation: list[dict]) -> dict:
        # pylint: disable=unused-argument
        if self.api_context.is_chat_completion:
            return self._call_chat_completion_api(conversation)

        return self._call_completion_api(conversation)

    @Logs.do_log_entry_and_exit()
    def _call_completion_api(self, conversation: list[dict]) -> dict:
        prompt = self._make_completion_prompt(conversation)

        response = self.client.completions.create(
            prompt=prompt,
            # api_type=self.api_context.type,
            # api_key=self.api_context.key,
            # api_base=self.api_context.base,
            # api_version=self.api_context.version,
            # engine=self.api_context.engine,
            model=self.api_context.model,
            max_tokens=self.api_context.max_tokens,
            temperature=self.api_context.temperature,
        )
        response = response.choices[0].text.strip()

        reply = self._parse_llm_response(response)
        if isinstance(reply, list):
            if len(reply) == 0 or len(reply[0]) == 0:
                reply = {"role": "assistant", "content": "I got nothing."}

        return reply

    @Logs.do_log_entry_and_exit()
    def _call_chat_completion_api(self, conversation: list[dict]) -> dict:
        response = self.client.chat.completions.create(
            messages=conversation,
            # api_type=self.api_context.type,
            # api_key=self.api_context.key,
            # api_base=self.api_context.base,
            # api_version=self.api_context.version,
            # model=self.api_context.model,
            # engine=self.api_context.engine,
            max_tokens=self.api_context.max_tokens,
            temperature=self.api_context.temperature,
        )

        response = response.choices[0].message.content
        return response


class GPT3CompletionSLM(SLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.is_chat_completion = False
        api_context.model = "text-davinci-002"
        api_context.engine = None
        super().__init__(api_context, adapter=adapter)


class GPT3CompletionSSM(BaseSSM):
    def __init__(
        self, adapter: AbstractAdapter = None, backends: list[AbstractBackend] = None
    ):
        super().__init__(GPT3CompletionSLM(), adapter, backends)


class GPT3ChatCompletionSLM(SLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        api_context.is_chat_completion = True
        api_context.model = "gpt-3.5-turbo"
        api_context.engine = None
        super().__init__(api_context, adapter=adapter)


class GPT3ChatCompletionSSM(BaseSSM):
    def __init__(
        self, adapter: AbstractAdapter = None, backends: list[AbstractBackend] = None
    ):
        super().__init__(GPT3ChatCompletionSLM(), adapter, backends)
