"""
================================
META LLAMA LANGUAGE MODELS (LMs)
================================
"""


from __future__ import annotations

from dataclasses import dataclass
import json
from typing import TYPE_CHECKING

from loguru import logger

from .config import LMConfig
from .openai import OpenAILM

if TYPE_CHECKING:
    from .abstract import LMChatHist


@dataclass
class LlamaLM(OpenAILM):
    """Llama LM."""

    @classmethod
    def from_defaults(cls) -> LlamaLM:
        """Get Llama LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=LMConfig.LLAMA_DEFAULT_MODEL, api_key=LMConfig.LLAMA_API_KEY, api_base=LMConfig.LLAMA_API_URL)

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call Llama LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})

        if json_format:
            kwargs['response_format'] = {'type': 'json_object'}

            while True:
                try:
                    response: str = self.call(messages, **kwargs).choices[0].message.content
                    response: str = response.replace('\n', '')  # TODO: fix Llama-generated JSONs more rigorously
                    return json.loads(response)

                except json.decoder.JSONDecodeError:
                    logger.debug(f'INVALID JSON, TO BE RETRIED:\n{response}')

        return self.call(messages, **kwargs).choices[0].message.content
