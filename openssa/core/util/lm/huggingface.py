"""
=================================
HUGGINGFACE LANGUAGE MODELS (LMs)
=================================
"""


from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import TYPE_CHECKING

from huggingface_hub.inference._client import InferenceClient

from .abstract import AbstractLM, LMChatHist
from .config import LMConfig

if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion


@dataclass
class HuggingFaceLM(AbstractLM):
    """HuggingFace LM."""

    client: InferenceClient = field(init=False)

    def __post_init__(self):
        """Initialize HuggingFace client."""
        self.client: InferenceClient = InferenceClient(model=self.model, token=self.api_key)

    @classmethod
    def from_defaults(cls) -> HuggingFaceLM:
        """Get HuggingFace LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=LMConfig.HF_DEFAULT_MODEL, api_key=LMConfig.HF_API_KEY, api_base=LMConfig.HF_API_URL)

    def call(self, messages: LMChatHist, **kwargs) -> ChatCompletion:
        """Call HuggingFace LM API and return response object."""
        return self.client.chat_completion(
            model=self.model,
            messages=messages,
            seed=kwargs.pop('seed', LMConfig.DEFAULT_SEED),
            temperature=kwargs.pop('temperature', LMConfig.DEFAULT_TEMPERATURE),
            max_tokens=6000,
            **kwargs)

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call HuggingFace LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})

        response_content: str = self.call(messages, **kwargs).choices[0].message.content
        response_content = response_content.replace("\n", " ")
        print(f"HF response_content = {response_content}")

        return json.loads(response_content) if json_format else response_content
