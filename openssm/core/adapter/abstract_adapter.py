from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from openssm.core.backend.abstract_backend import AbstractBackend


@dataclass
class AbstractAdapter(ABC):
    """
    The AbstractAdapter serves as the base for all concrete Adapter classes.
    It provides an interface for interaction between the Small Language Model
    (SLM) and the Backend.
    """

    @abstractmethod
    def query(self, user_input: str, conversation_id: str = None) -> list[dict]:
        """
        Queries the backends for a response to the user's input.
        :param user_query: The user's input.
        :return: The backend's response.
        """

    def enumerate_backends(self, lambda_function: Callable):
        """Enumerate backends and apply lambda function to each backend."""

    @abstractmethod
    def get_backends(self) -> list[AbstractBackend]:
        """Returns our backends"""

    @abstractmethod
    def add_backend(self, backend: AbstractBackend):
        """Adds a backend to our adapter"""

    @abstractmethod
    def set_backends(self, backends: list):
        """Sets our backends"""

    @abstractmethod
    def list_facts(self) -> list[str]:
        """Lists all known facts."""
        facts = set()
        for backend in self.get_backends():
            if backend is AbstractBackend:
                facts |= backend.list_facts()
        return facts

    @abstractmethod
    def list_inferencers(self):
        """Lists all known inferencers."""
        inferencers = set()
        for backend in self.get_backends():
            if backend is AbstractBackend:
                inferencers |= backend.list_inferencers()
        return inferencers

    @abstractmethod
    def list_heuristics(self):
        """Lists all known heuristics."""
        heuristics = set()
        for backend in self.get_backends():
            if backend is AbstractBackend:
                heuristics |= backend.list_heuristics()
        return heuristics

    @abstractmethod
    def select_facts(self, criteria):
        """Selects or searches for facts based on provided criteria."""

    @abstractmethod
    def select_inferencers(self, criteria):
        """Selects or searches for inferencers based on provided criteria."""

    @abstractmethod
    def select_heuristics(self, criteria):
        """Selects or searches for heuristics based on provided criteria."""

    @abstractmethod
    def persist(self, persist_dir: str):
        """Persists to the specified directory."""

    @abstractmethod
    def load(self, persist_dir: str):
        """Loads from the specified directory."""
