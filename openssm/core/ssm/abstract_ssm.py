from abc import ABC, abstractmethod
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class AbstractSSM(ABC):
    """
    The AbstractSSM serves as the base for all concrete Small Specialist
    Models (SSMs).
    """

    @abstractmethod
    def get_slm(self) -> AbstractSLM:
        """Returns our small language model (SLM)"""

    @abstractmethod
    def get_adapter(self) -> AbstractAdapter:
        """Returns our adapter"""

    @abstractmethod
    def get_backends(self) -> list[AbstractBackend]:
        """Returns our backends"""

    @abstractmethod
    def discuss(self,
                conversation_id: str,
                user_input: list[dict]) -> list[dict]:
        """Processes a natural language conversation input."""

    @abstractmethod
    def api_call(self, function_name, *args, **kwargs):
        """Processes a structured API call."""

    @abstractmethod
    def reset_memory(self):
        """Resets the conversation memory of the SSM."""

    @abstractmethod
    def list_facts(self) -> list[str]:
        """Lists all known facts."""

    @abstractmethod
    def list_inferencers(self) -> list[str]:
        """Lists all known inferencers."""

    @abstractmethod
    def list_heuristics(self) -> list[str]:
        """Lists all known heuristics."""

    @abstractmethod
    def select_facts(self, criteria: dict) -> list[str]:
        """Selects or searches for facts based on provided criteria."""

    @abstractmethod
    def select_inferencers(self, criteria: dict) -> list[str]:
        """Selects or searches for inferencers based on provided criteria."""

    @abstractmethod
    def select_heuristics(self, criteria) -> list[str]:
        """Selects or searches for heuristics based on provided criteria."""

    @abstractmethod
    def infer(self, input_facts: list[str]) -> list[str]:
        """Makes inferences based on the provided input facts."""

    @abstractmethod
    def solve_problem(self, problem_description: list[str]) -> list[str]:
        """Solves a problem based on the provided description."""

    @abstractmethod
    def add_backend(self, backend: AbstractBackend):
        """Adds a backend to the SSM."""
