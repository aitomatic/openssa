from abc import ABC, abstractmethod
from dataclasses import dataclass
from openssm.core.inferencer.abstract_inferencer import AbstractInferencer


# pylint: disable=duplicate-code
@dataclass
class AbstractBackend(ABC):
    @abstractmethod
    def query(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        Queries the backend with the user input.
        """
        pass

    @abstractmethod
    def load_all(self):
        """
        Loads all facts, inferencers, and heuristics,
        if appropriate. Some backends may not need to,
        and only load on demand (e.g., a database backend).
        """
        pass

    @abstractmethod
    def add_fact(self, fact: str):
        pass

    @abstractmethod
    def add_inferencer(self, inferencer: AbstractInferencer):
        pass

    @abstractmethod
    def add_heuristic(self, heuristic: str):
        pass

    @abstractmethod
    def list_facts(self):
        pass

    @abstractmethod
    def list_inferencers(self):
        pass

    @abstractmethod
    def list_heuristics(self):
        pass

    @abstractmethod
    def select_facts(self, criteria):
        pass

    @abstractmethod
    def select_inferencers(self, criteria):
        pass

    @abstractmethod
    def select_heuristics(self, criteria):
        pass

    @abstractmethod
    def save(self, storage_dir: str):
        """Saves to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads from the specified directory."""
