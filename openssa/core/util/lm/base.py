"""
=============================
LANGUAGE MODEL (LM) INTERFACE
=============================
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self as SameType

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
# - github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_system_message_param.py
# - github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_user_message_param.py
# - github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_assistant_message_param.py
# - github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_tool_message_param.py
# - github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_function_message_param.py


type LMChatHist = list[ChatCompletionMessageParam]


@dataclass
class BaseLM(ABC):
    """Abstract base class for consistent API for different LM services."""

    model: str
    api_base: str
    api_key: str = field(default_factory=str,
                         init=True,
                         repr=False,
                         hash=None,
                         compare=True,
                         metadata=None,
                         kw_only=False)

    @classmethod
    @abstractmethod
    def from_defaults(cls) -> SameType:
        """Get LM instance with default parameters."""

    @abstractmethod
    def call(self, messages: list[ChatCompletionMessageParam], **kwargs):
        """Call LM API and return response object."""

    @abstractmethod
    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call LM API and return response content."""
