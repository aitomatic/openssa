from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
from typing import Literal, Self, TypedDict

from llamaapi import LlamaAPI
from openai import OpenAI

from openssa.l2.config import Config


class LMChatMsg(TypedDict):
    role: Literal['system', 'user', 'assistant', 'tool', 'function']
    content: str


type LMChatHist = list[LMChatMsg]


@dataclass
class AnLM(ABC):
    """Abstract base class for consistent API for different LM services."""

    model: str
    api_key: str
    api_base: str

    @classmethod
    @abstractmethod
    def from_defaults(cls) -> Self:
        """Get LM instance with default parameters."""

    @abstractmethod
    def call(self, messages: list[LMChatMsg], **kwargs):
        """Call LM API and return response object."""

    @abstractmethod
    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call LM API and return response content."""


@dataclass
class LlamaLM(AnLM):
    """Llama LM."""

    client: LlamaAPI = field(init=False)

    def __post_init__(self):
        """Initialize Llama LM client."""
        self.client: LlamaAPI = LlamaAPI(api_token=self.api_key, hostname=self.api_base)

    @classmethod
    def from_defaults(cls) -> LlamaLM:
        """Get Llama LM instance with default parameters."""
        return cls(model=Config.DEFAULT_LLAMA_MODEL, api_key=Config.LLAMA_API_KEY, api_base=Config.LLAMA_API_URL)

    def call(self, messages: list[LMChatMsg], **kwargs):
        """Call Llama LM API and return response object."""
        return self.client.run({'model': self.model,
                                'messages': messages,
                                'temperature': kwargs.pop('temperature', Config.DEFAULT_TEMPERATURE),
                                **kwargs})

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call Llama LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({"role": "user", "content": prompt})
        return self.call(messages, **kwargs)["choices"][0]["message"]["content"]


@dataclass
class OpenAILM(AnLM):
    """OpenAI LM."""

    client: OpenAI = field(init=False)

    def __post_init__(self):
        """Initialize OpenAI client."""
        self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls):
        """Get OpenAI LM instance with default parameters."""
        return cls(model=Config.DEFAULT_OPENAI_MODEL, api_key=Config.OPENAI_API_KEY, api_base=Config.OPENAI_API_URL)

    def call(self, messages: list[LMChatMsg], **kwargs):
        """Call OpenAI LM API and return response object."""
        return self.client.chat.completions.create(model=self.model,
                                                   messages=messages,
                                                   temperature=kwargs.pop('temperature', Config.DEFAULT_TEMPERATURE),
                                                   **kwargs)

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call OpenAI LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({"role": "user", "content": prompt})

        if json_format:
            kwargs['response_format'] = {'type': 'json_object'}

        response_content: str = self.call(messages, **kwargs).choices[0].message.content

        return json.loads(response_content) if json_format else response_content
