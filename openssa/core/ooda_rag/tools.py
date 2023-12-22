from abc import ABC, abstractmethod
import traceback
from json import JSONDecodeError

from httpx import RequestError, TimeoutException, HTTPStatusError
from openssa.core.ssm.rag_ssm import RAGSSM
from openssa.core.ssa.ssa import RagSSA


class Tool(ABC):
    """
    Abstract base class for all tools.
    """

    def __init__(self, description: str) -> None:
        self._description = description

    @abstractmethod
    def execute(self, question: str):
        """
        Execute the tool with the given arguments.
        """
        pass

    @property
    def description(self) -> str:
        """
        Return a description of the tool's functionality.
        """
        return self._description


class AskUserTool(Tool):
    """
    A tool for asking the user a question.
    """

    def __init__(self) -> None:
        super().__init__("Ask the user for personal information.")

    def execute(self, question: str) -> str:
        """
        Ask the user for personal information.

        :param question (str): The question to ask the user.
        :return (str): The user's answer to the question.
        """
        return input(question)


class ResearchDocumentsTool(Tool):
    """
    A tool for querying a document base for information.
    """

    def __init__(self, agent_id: str) -> None:
        description = "Query a document base for factual information."
        super().__init__(description)
        self.agent_id = agent_id

    def execute(self, question: str) -> str:
        """
        Query a document base for factual information.

        :param question (str): The question to ask the document base.
        :return (str): The answer to the question.
        """
        try:
            return RagSSA().chat(self.agent_id, question)
        except (RequestError, TimeoutException, HTTPStatusError, JSONDecodeError) as e:
            traceback.print_exc()
            print(f"An error occurred while querying the document base: {e}")
            return ""


class ReasearchAgentTool(Tool):
    """
    A tool for querying a document base for information.
    """

    def __init__(self, agent: RAGSSM) -> None:
        description = "Query a document base for factual information."
        super().__init__(description)
        self.agent = agent


    def execute(self, question: str) -> str:
        """
        Query a document base for factual information.

        :param question (str): The question to ask the document base.
        :return (str): The answer to the question.
        """
        response =  self.agent.discuss(question)
        print(f"debug: {response}")
        return response
