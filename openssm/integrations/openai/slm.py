import os
from abc import ABC
from typing import Optional
import openai
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.slm.base_slm import BaseSLM
from openssm.utils.config import Config
from openssm.utils.logs import Logs


Config.OPENAI_API_KEY: Optional[str] = os.environ.get('OPENAI_API_KEY') or None
Config.OPENAI_API_URL: Optional[str] = os.environ.get('OPENAI_API_URL') or "https://api.openai.com/v1"


class _AbstractSLM(BaseSLM, ABC):
    def __init__(self,
                 api_key: str = Config.OPENAI_API_KEY,
                 api_base: str = Config.OPENAI_API_URL,
                 model: str = None,
                 adapter: AbstractAdapter = None):
        super().__init__(adapter)
        if api_key is None:
            raise ValueError("api_key must be provided, e.g., via Config.OPENAI_API_KEY or 'sk-xxxxx'")

        if model is None:
            raise ValueError("model must be provided (e.g., 'gpt-3.5-turbo'))")

        self.api_key = api_key
        self.api_base = api_base
        self.model = model


class ChatCompletionSLM(_AbstractSLM):
    def __init__(self,
                 api_key: str = Config.OPENAI_API_KEY,
                 api_base: str = Config.OPENAI_API_URL,
                 model: str = "gpt-3.5-turbo",
                 adapter: AbstractAdapter = None):
        super().__init__(api_key, api_base, model, adapter)

    @Logs.do_log_entry_and_exit()
    def _call_lm_api(self, conversation: list[dict]) -> list[dict]:
        response = openai.ChatCompletion.create(
            api_key=self.api_key,
            api_base=self.api_base,
            model=self.model,
            messages=conversation,
            # max_tokens=150,
            temperature=0.7
        )
        return [response.choices[0].message]

class GPT3ChatCompletionSLM(ChatCompletionSLM):
    def __init__(self,
                 api_key: str = Config.OPENAI_API_KEY,
                 api_base: str = Config.OPENAI_API_URL,
                 adapter: AbstractAdapter = None):
        super().__init__(api_key=api_key, api_base=api_base, model="gpt-3.5-turbo", adapter=adapter)


class CompletionSLM(_AbstractSLM):
    def __init__(self,
                 api_key: str = Config.OPENAI_API_KEY,
                 api_base: str = Config.OPENAI_API_URL,
                 model: str = "text-davinci-002",
                 adapter: AbstractAdapter = None):
        super().__init__(api_key, api_base, model, adapter)

    @Logs.do_log_entry_and_exit()
    def _call_lm_api(self, conversation: list[dict]) -> list[dict]:
        prompt = self._make_completion_prompt(conversation)

        openai.api_key = self.api_key
        openai.api_base = self.api_base

        response = openai.Completion.create(
            api_key=self.api_key,
            api_base=self.api_base,
            engine=self.model,
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )
        response = response.choices[0].text.strip()

        replies = self._parse_llm_response(response)

        if len(replies) == 0 or len(replies[0]) == 0:
            replies = [{'role': 'assistant', 'content': 'I got nothing.'}]

        return replies

class GPT3CompletionSLM(CompletionSLM):
    def __init__(self,
                 api_key: str = Config.OPENAI_API_KEY,
                 api_base: str = Config.OPENAI_API_URL,
                 adapter: AbstractAdapter = None):
        super().__init__(api_key=api_key, api_base=api_base, model="text-davinci-002", adapter=adapter)
