from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from openssa.core.backend.abstract_backend import AbstractBackend


@dataclass
class AbstractAdapter(ABC):
    """
    The AbstractAdapter serves as the base for all concrete Adapter classes.
    It provides an interface for interaction between the Small Language Model
    (SLM) and the Backend.
    """

    @abstractmethod
    def query_all(self, user_input: str, conversation: list[dict] = None) -> list[dict]:
        """
        Queries the backends for a response to the user's input.
        :param user_query: The user's input.
        :return: The backend's response.
        """

    def enumerate_backends(self, lambda_function: Callable):
        """Enumerate backends and apply lambda function to each backend."""

    @property
    @abstractmethod
    def backends(self) -> list[AbstractBackend]:
        """Returns our backends"""

    @backends.setter
    @abstractmethod
    def backends(self, backends: list):
        """Sets our backends"""

    @abstractmethod
    def add_backend(self, backend: AbstractBackend):
        """Adds a backend to our adapter"""

    @property
    @abstractmethod
    def facts(self) -> list[str]:
        """Lists all known facts."""

    @property
    @abstractmethod
    def inferencers(self):
        """Lists all known inferencers."""

    @property
    @abstractmethod
    def heuristics(self):
        """Lists all known heuristics."""

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
    def save(self, storage_dir: str):
        """Saves to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads from the specified directory."""
