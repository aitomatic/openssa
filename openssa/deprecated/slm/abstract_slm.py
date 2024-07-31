from abc import ABC, abstractmethod
from dataclasses import dataclass
from openssa.core.adapter.abstract_adapter import AbstractAdapter


@dataclass
class AbstractSLM(ABC):
    """
    The AbstractSLM serves as the base for all concrete Small Language Models
    (SLMs). It provides an interface for natural language communication and
    structured API interactions.
    """

    @property
    @abstractmethod
    def adapter(self) -> AbstractAdapter:
        """Returns our adapter"""

    @adapter.setter
    @abstractmethod
    def adapter(self, adapter: AbstractAdapter):
        """Sets our adapter"""

    @abstractmethod
    def do_discuss(self, user_input: list[dict], conversation: list[dict]) -> dict:
        """
        Processes a natural language conversation input
        and returns a dict of the reply. Not intended for direct use.
        """

    @abstractmethod
    def save(self, storage_dir: str):
        """Saves to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads from the specified directory."""
