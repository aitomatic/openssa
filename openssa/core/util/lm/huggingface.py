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

    # client: OpenAI = field(init=False)
    client: InferenceClient = field(init=False)

    def __post_init__(self):
        """Initialize HuggingFace client."""
        # self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.api_base)
        print("Initialized LM through HF!")
        print(f"LMConfig.HF_API_KEY = {LMConfig.HF_API_KEY}")
        self.client: InferenceClient = InferenceClient(model=LMConfig.DEFAULT_HF_LLAMA_MODEL, token=LMConfig.HF_API_KEY)

    @classmethod
    def from_defaults(cls) -> HuggingFaceLM:
        """Get HuggingFace LM instance with default parameters."""
        return cls(model=LMConfig.DEFAULT_HF_LLAMA_MODEL, api_key=LMConfig.HF_API_KEY, api_base=LMConfig.HF_API_URL)

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
