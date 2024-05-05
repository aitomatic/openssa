from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Self, TypedDict, TypeVar


class LMChatMsg(TypedDict):
    role: Literal['system', 'user', 'assistant', 'tool', 'function']
    content: str


type LMChatHist = list[LMChatMsg]


@dataclass
class AbstractLM(ABC):
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


AnLM: TypeVar = TypeVar('AnLM', bound=AbstractLM, covariant=False, contravariant=False)
