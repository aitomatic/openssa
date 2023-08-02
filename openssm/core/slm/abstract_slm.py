from abc import ABC, abstractmethod
from dataclasses import dataclass
from openssm.core.adapter.abstract_adapter import AbstractAdapter


@dataclass
class AbstractSLM(ABC):
    """
    The AbstractSLM serves as the base for all concrete Small Language Models
    (SLMs). It provides an interface for natural language communication and
    structured API interactions.
    """

    @abstractmethod
    def get_adapter(self) -> AbstractAdapter:
        """Returns our adapter"""

    @abstractmethod
    def set_adapter(self, adapter: AbstractAdapter):
        """Sets our adapter"""

    @abstractmethod
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        Processes a natural language conversation input
        and returns a list of replies
        """

    @abstractmethod
    def reset_memory(self):
        """Resets our conversation memory"""

    @abstractmethod
    def save(self, storage_dir: str):
        """Saves to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads from the specified directory."""
