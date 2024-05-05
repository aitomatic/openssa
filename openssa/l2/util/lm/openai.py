from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import TYPE_CHECKING

from openai import OpenAI  # pylint: disable=import-self

from openssa.l2.config import Config
from .abstract import AbstractLM, LMChatMsg, LMChatHist

if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion


@dataclass
class OpenAILM(AbstractLM):
    """OpenAI LM."""

    client: OpenAI = field(init=False)

    def __post_init__(self):
        """Initialize OpenAI client."""
        self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls) -> OpenAILM:
        """Get OpenAI LM instance with default parameters."""
        return cls(model=Config.DEFAULT_OPENAI_MODEL, api_key=Config.OPENAI_API_KEY, api_base=Config.OPENAI_API_URL)

    def call(self, messages: list[LMChatMsg], **kwargs) -> ChatCompletion:
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
