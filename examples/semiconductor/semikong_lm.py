from __future__ import annotations

from dataclasses import dataclass, field

from openai import OpenAI

from openssa.core.util.lm.abstract import AbstractLM, LMChatHist
from openssa.core.util.lm.config import LMConfig

DEFAULT_MODEL = "pentagoniac/SEMIKONG-70B"
DEFAULT_API_KEY = "dummy"
DEFAULT_API_BASE = "http://34.44.90.64:8081/v1"

@dataclass
class SemiKongLM(AbstractLM):
    """SemiKong LM."""

    client: OpenAI = field(init=False)
    # inherited: model [str], api_base[str], api_key[str]

    def __post_init__(self):
        """Initialize SemiKong LM client."""
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls) -> None:
        """Get default SemiKong LM instance."""
        return cls(model=DEFAULT_MODEL, api_key=DEFAULT_API_KEY, api_base=DEFAULT_API_BASE)

    def call(self, messages: LMChatHist, **kwargs):
        """Call SemiKong LM endpoint and return response object."""
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=LMConfig.DEFAULT_TEMPERATURE,
            **kwargs
        )

    def get_response(
        self,
        prompt: str,
        history: LMChatHist | None = None,
        json_format: bool = False,
        **kwargs
    ) -> str:
        # pylint: disable=unused-argument
        """Call LM endpoint and return response content."""
        messages: LMChatHist = history or []
        messages.append({"role": "user", "content": prompt})
        answer = self.call(messages, **kwargs).choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        return answer
