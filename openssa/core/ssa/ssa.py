from abc import ABC, abstractmethod
from .ssa_service import SSAService, SSARAGService


class AbstractSSA(ABC):
    """Abstract class for Small Specialist Agents."""

    @classmethod
    @abstractmethod
    def train(cls, document_path: str) -> str:
        """
        Train a Small Specialist Agent in the backend.

        Args:
            document_path (str): Path to the document to train the agent.
        Returns:
            str: Training session ID.
        """
        pass

    @classmethod
    @abstractmethod
    def load(cls, training_session_id: str) -> "AbstractSSA":
        """
        Load a trained Small Specialist Agent from the backend.

        Args:
            training_session_id (str): Training session ID.
        Returns:
            AbstractSSA: Trained agent.
        """
        pass

    @abstractmethod
    def chat(self, message: str) -> str:
        """Chat with a Small Specialist Agent."""


class BaseSSA(AbstractSSA):
    """Base class for Small Specialist Agents."""

    def __init__(self):
        pass

    @classmethod
    def train(cls, document_path: str) -> str:
        return SSAService.train(document_path)

    @classmethod
    def load(cls, training_session_id: str) -> AbstractSSA:
        # waiting on Chanh's endpoint to get objects and build agent here
        pass

    def chat(self, message: str, config: dict = None) -> str:
        """Chat with a Small Specialist Agent."""
        config = config or {}
        return SSAService.chat(message, config)


class RagSSA():
    def __init__(self):
        pass

    @classmethod
    def train(cls, agent_id: str, s3_source_path: str, **kwargs) -> str:
        return SSARAGService.create_rag_agent(agent_id, s3_source_path, **kwargs)

    def chat(self, agent_id: str, message: str) -> str:
        """Chat with a Small Specialist Agent."""
        return SSARAGService.chat(agent_id, message)

    def add_knowledge(self, agent_id: str, message: str) -> str:
        """Add knowledge to a Small Specialist Agent."""
        return SSARAGService.add_knowledge(agent_id, message)
