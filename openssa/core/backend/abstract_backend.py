from abc import ABC, abstractmethod
from dataclasses import dataclass
from openssa.core.inferencer.abstract_inferencer import AbstractInferencer


# pylint: disable=duplicate-code
@dataclass
class AbstractBackend(ABC):
    @abstractmethod
    def query(self, user_input: list[dict], conversation: list[dict] = None) -> dict:
        """
        Queries the backend with the user input.
        Response may be in the form {"response": "some response", "response_object": some_object}
        """

    @abstractmethod
    def load_all(self):
        """
        Loads all facts, inferencers, and heuristics,
        if appropriate. Some backends may not need to,
        and only load on demand (e.g., a database backend).
        """

    @abstractmethod
    def add_fact(self, fact: str):
        """Adds a fact to the backend."""

    @abstractmethod
    def add_inferencer(self, inferencer: AbstractInferencer):
        """Adds an inferencer to the backend."""

    @abstractmethod
    def add_heuristic(self, heuristic: str):
        """Adds a heuristic to the backend."""

    @property
    @abstractmethod
    def facts(self):
        """Returns a set of facts."""

    @property
    @abstractmethod
    def inferencers(self):
        """Returns a set of inferencers."""

    @property
    @abstractmethod
    def heuristics(self):
        """Returns a set of heuristics."""

    @abstractmethod
    def select_facts(self, criteria):
        """Returns a set of facts that match the criteria."""

    @abstractmethod
    def select_inferencers(self, criteria):
        """Returns a set of inferencers that match the criteria."""

    @abstractmethod
    def select_heuristics(self, criteria):
        """Returns a set of heuristics that match the criteria."""

    @abstractmethod
    def save(self, storage_dir: str):
        """Saves to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads from the specified directory."""
