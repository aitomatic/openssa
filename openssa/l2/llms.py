from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from llamaapi import LlamaAPI
from openai import OpenAI
from openssa.l2.config import Config


@dataclass
class AnLLM(ABC):
    """
    This class provides a consistent API for the different LLM services.
    """
    model: str
    api_key: str
    api_base: str

    @classmethod
    @abstractmethod
    def from_defaults(cls):
        """Get an LLM instance with default parameters."""

    @abstractmethod
    def call(self, messages: list, **kwargs):
        """Call the LLM API and return the response object."""

    @abstractmethod
    def get_response(self, prompt: str, messages: list = None, **kwargs):
        """Call the LLM API and return the response content."""


@dataclass
class LlamaLLM(AnLLM):
    """Use the Llama client."""
    client: LlamaAPI = field(init=False)

    def __post_init__(self):
        """Initialize the Llama client."""
        self.client = LlamaAPI(api_token=self.api_key, hostname=self.api_base)

    @classmethod
    def from_defaults(cls) -> LlamaLLM:
        """Get an LlamaLLM instance with default parameters."""
        return cls(model=Config.DEFAULT_LLAMA_MODEL, api_key=Config.LLAMA_API_KEY, api_base=Config.LLAMA_API_URL)

    def call(self, messages: list, **kwargs):
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


@dataclass
class OpenAILLM(AnLLM):
    """Use the OpenAI client."""

    client: OpenAI = field(init=False)

    def __post_init__(self):
        """Initialize the OpenAI client."""
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls):
        """Get an OpenAILLM instance with default parameters."""
        return cls(model=Config.DEFAULT_OPENAI_MODEL, api_key=Config.OPENAI_API_KEY, api_base=Config.OPENAI_API_URL)

    def call(self, messages: list, **kwargs):
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
