"""
================================
META LLAMA LANGUAGE MODELS (LMs)
================================
"""


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .config import LMConfig
from .openai import OpenAILM

if TYPE_CHECKING:
    from .base import LMChatHist


@dataclass
class LlamaLM(OpenAILM):
    """Llama LM."""

    @classmethod
    def from_defaults(cls) -> LlamaLM:
        """Get Llama LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=LMConfig.LLAMA_DEFAULT_MODEL, api_key=LMConfig.LLAMA_API_KEY, api_base=LMConfig.LLAMA_API_URL)
