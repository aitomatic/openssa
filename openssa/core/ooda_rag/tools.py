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
    def execute(self, task: str):
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

    def execute(self, task: str) -> str:
        """
        Ask the user for personal information.

        :param task (str): The question to ask the user.
        :return (str): The user's answer to the question.
        """
        return input(task)


class ResearchDocumentsTool(Tool):
    """
    A tool for querying a document base for information.
    """

    def __init__(self, agent_id: str) -> None:
        description = "Query a document base for factual information."
        super().__init__(description)
        self.agent_id = agent_id

    def execute(self, task: str) -> dict:
        """
        Query a document base for factual information.

        :param task (str): The question to ask the document base.
        :return (dict): The answer to the question including content and citations
        """
        try:
            response = RagSSA().chat(self.agent_id, task)
            return response.get("message", {})
        except (RequestError, TimeoutException, HTTPStatusError, JSONDecodeError) as e:
            traceback.print_exc()
            print(f"An error occurred while querying the document base: {e}")
            return {}


class ReasearchAgentTool(Tool):
    """
    A tool for querying a document base for information.
    """

    def __init__(self, agent: RAGSSM) -> None:
        description = "Query a document base for factual information."
        super().__init__(description)
        self.agent = agent

    def execute(self, task: str) -> dict:
        """
        Query a document base for factual information.

        :param task (str): The question to ask the document base.
        :return (dict): The answer to the question.
        """
        response = self.agent.discuss(task)
        print(f"debug: {response}")
        return response


class PythonCodeTool(Tool):
    """
    A tool for executing python code.
    """

    def __init__(self) -> None:
        super().__init__("Execute python code.")

    def execute(self, task: str) -> str:
        """
        Execute python code.

        :param task (str): The python code to execute.
        :return (str): The result of the code execution.
        """
        print(f"Executing python code: {task}")
        return ""


class ResearchQueryEngineTool(Tool):
    """
    A tool for querying a document base for information.
    """

    def __init__(self, query_engine) -> None:
        description = "Query a document base for factual information."
        super().__init__(description)
        self.query_engine = query_engine

    def get_citations(self, metadata: dict):
        citations = []
        for data in metadata.values():
            citations.append(
                {
                    "source": data.get("file_path", ""),
                    "pages": [data.get("page_label", "")],
                    "type": data.get("file_type").split("/")[-1],
                }
            )
        return citations

    def execute(self, question: str) -> dict:
        """
        Query a document base for factual information.

        :param question (str): The question to ask the document base.
        :return (dict): The answer to the question.
        """
        response = self.query_engine.query(question)
        content = response.response
        citations = self.get_citations(response.metadata)
        return {"content": content, "citations": citations}
