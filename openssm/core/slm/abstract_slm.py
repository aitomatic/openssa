from abc import ABC, abstractmethod
from ..adapter.abstract_adapter import AbstractAdapter


class AbstractSLM(ABC):
    """
    The AbstractSLM serves as the base for all concrete Small Language Models
    (SLMs). It provides an interface for natural language communication and
    structured API interactions.
    """

    @abstractmethod
    def get_adapter(self) -> AbstractAdapter:
        """Returns our adapter"""
        pass

    @abstractmethod
    def set_adapter(self, adapter: AbstractAdapter):
        """Sets our adapter"""
        pass

    @abstractmethod
    def discuss(self,
                conversation_id: str,
                user_input: list[dict]) -> list[dict]:
        """
        Processes a natural language conversation input
        and returns a list of replies
        """
        pass

    @abstractmethod
    def reset_memory(self):
        """Resets our conversation memory"""
        pass
