"""
==============
Meta Llama LMs
==============
"""


from __future__ import annotations

from dataclasses import dataclass, field

from llamaapi import LlamaAPI

from .abstract import AbstractLM, LMChatHist
from .config import LMConfig


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
        return cls(model=LMConfig.DEFAULT_LLAMA_MODEL, api_key=LMConfig.LLAMA_API_KEY, api_base=LMConfig.LLAMA_API_URL)

    def call(self, messages: LMChatHist, **kwargs):
        """Call Llama LM API and return response object."""
        return self.client.run({'model': self.model,
                                'messages': messages,
                                'temperature': kwargs.pop('temperature', LMConfig.DEFAULT_TEMPERATURE),
                                **kwargs})

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        # pylint: disable=unused-argument
        """Call Llama LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})
        return self.call(messages, **kwargs)['choices'][0]['message']['content']
