from __future__ import annotations

from dataclasses import dataclass, field

from llamaapi import LlamaAPI

from openssa.l2.config import Config
from .abstract import AbstractLM, LMChatHist


@dataclass
class LlamaLM(AbstractLM):
    """Llama LM."""

    client: LlamaAPI = field(init=False)

    def __post_init__(self):
        """Initialize Llama LM client."""
        self.client: LlamaAPI = LlamaAPI(api_token=self.api_key, hostname=self.api_base)

    @classmethod
    def from_defaults(cls) -> LlamaLM:
        """Get Llama LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=Config.DEFAULT_LLAMA_MODEL, api_key=Config.LLAMA_API_KEY, api_base=Config.LLAMA_API_URL)

    def call(self, messages: LMChatHist, **kwargs):
        """Call Llama LM API and return response object."""
        return self.client.run({'model': self.model,
                                'messages': messages,
                                'temperature': kwargs.pop('temperature', Config.DEFAULT_TEMPERATURE),
                                **kwargs})

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        # pylint: disable=unused-argument
        """Call Llama LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})
        return self.call(messages, **kwargs)['choices'][0]['message']['content']
