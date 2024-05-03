from __future__ import annotations

from typing import Dict, List

from llamaapi import LlamaAPI
from openai import OpenAI

from openssa.l2.config import Config

class AnLLM:
    """
    This class provides a consistent API for the different LLM services.
    """
    def __init__(
        self,
        model: str,
        api_key: str,
        api_base: str,
    ):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base

    @classmethod
    def from_defaults(cls):
        """Get an LLM instance with default parameters."""
        pass

    def call(self, messages: List[Dict], **kwargs):
        """Call the LLM API and return the response object."""
        pass


class LlamaLLM(AnLLM):
    """Use the Llama client."""
    def __init__(
        self,
        model: str = Config.DEFAULT_LLAMA_MODEL,
        api_key: str = Config.LLAMA_API_KEY,
        api_base: str = Config.LLAMA_API_URL,
    ):
        super().__init__(model, api_key, api_base)
        self.client = LlamaAPI(api_token=self.api_key, hostname=self.api_base)

    @classmethod
    def from_defaults(cls):
        return cls()

    def call(self, messages: List[Dict], **kwargs):
        return self.client.run({
            "model": self.model,
            "messages": messages,
            "temperature": Config.DEFAULT_TEMPERATURE,
            **kwargs,
        })

    def get_response(self, prompt: str, messages: list = None, **kwargs):
        messages = messages if messages else []
        messages.append({"role": "user", "content": prompt})
        return self.call(messages, **kwargs)["choices"][0]["message"]["content"]

class OpenAILLM(AnLLM):
    """Use the OpenAI client."""
    def __init__(
        self,
        model: str = Config.DEFAULT_OPENAI_MODEL,
        api_key: str = Config.OPENAI_API_KEY,
        api_base: str = Config.OPENAI_API_URL,
    ):
        super().__init__(model, api_key, api_base)
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls):
        return cls()

    def call(self, messages: List[Dict], **kwargs):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=Config.DEFAULT_TEMPERATURE,
            **kwargs,
        )

    def get_response(self, prompt: str, messages: list = None, **kwargs):
        messages = messages if messages else []
        messages.append({"role": "user", "content": prompt})
        return self.call(messages, **kwargs).choices[0].message.content
