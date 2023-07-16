from abc import ABC, abstractmethod
from openssm.core.backend.abstract_backend import AbstractBackend


class AbstractAdapter(ABC):
    """
    The AbstractAdapter serves as the base for all concrete Adapter classes.
    It provides an interface for interaction between the Small Language Model
    (SLM) and the Backend.
    """

    @abstractmethod
    def query(self, conversation_id: str, user_input: str) -> list({}):
        """
        Queries the backends for a response to the user's input.
        :param user_query: The user's input.
        :return: The backend's response.
        """

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
                facts.add(backend.list_facts())
        return facts

    @abstractmethod
    def list_inferencers(self):
        """Lists all known inferencers."""
        inferencers = set()
        for backend in self.get_backends():
            if backend is AbstractBackend:
                inferencers.add(backend.list_inferencers())
        return inferencers

    @abstractmethod
    def list_heuristics(self):
        """Lists all known heuristics."""
        heuristics = set()
        for backend in self.get_backends():
            if backend is AbstractBackend:
                heuristics.add(backend.list_inferencers())
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
