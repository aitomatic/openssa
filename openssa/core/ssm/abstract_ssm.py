from abc import ABC, abstractmethod
from dataclasses import dataclass
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.core.backend.abstract_backend import AbstractBackend


@dataclass
class AbstractSSM(ABC):
    """
    The AbstractSSM serves as the base for all concrete Small Specialist
    Models (SSMs).
    """

    @property
    @abstractmethod
    def slm(self) -> AbstractSLM:
        """Returns our small language model (SLM)"""

    @slm.setter
    @abstractmethod
    def slm(self, slm: AbstractSLM):
        """Sets our small language model (SLM)"""

    @property
    @abstractmethod
    def adapter(self) -> AbstractAdapter:
        """Returns our adapter"""

    @adapter.setter
    @abstractmethod
    def adapter(self, adapter: AbstractAdapter):
        """Sets our adapter"""

    @property
    @abstractmethod
    def backends(self) -> list[AbstractBackend]:
        """Returns our backends"""

    @backends.setter
    @abstractmethod
    def backends(self, backends: list[AbstractBackend]):
        """Sets our backends"""

    @abstractmethod
    def api_call(self, function_name, *args, **kwargs):
        """Processes a structured API call."""

    @abstractmethod
    def reset_memory(self):
        """Resets the conversation memory of the SSM."""

    @property
    @abstractmethod
    def facts(self) -> list[str]:
        """Lists all known facts."""

    @property
    @abstractmethod
    def inferencers(self) -> list[str]:
        """Lists all known inferencers."""

    @property
    @abstractmethod
    def heuristics(self) -> list[str]:
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
    def add_knowledge(self, knowledge_source_uri: str, knowledge_type=None):
        """Uploads a knowledge source (documents, text, files, etc.)"""

    @abstractmethod
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> dict:
        """Processes a natural language conversation input."""

    @abstractmethod
    def save(self, storage_dir: str):
        """Saves the SSM to the specified directory."""

    @abstractmethod
    def load(self, storage_dir: str):
        """Loads the SSM from the specified directory."""
