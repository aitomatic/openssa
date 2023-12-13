from abc import ABC, abstractmethod
from typing import List, Optional
import json
from openai import OpenAI
from loguru import logger
from openssa.utils.aitomatic_llm_config import AitomaticLLMConfig
from openssa.core.ooda_rag.prompts import BuiltInAgentPrompt
from openssa.utils.utils import Utils


class AgentRole:
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class TaskAgent(ABC):
    """
    Abstract base class for all task agents.
    """

    @abstractmethod
    def execute(self, task: str) -> str:
        """
        Execute the task agent with the given task.
        """
        pass


class AskUserAgent(TaskAgent):
    """
    AskUserAgent helps to determine if user wants to provide additional information
    """

    def __init__(
        self,
        llm: OpenAI = AitomaticLLMConfig.get_aitomatic_llm(),
        model: str = "aitomatic-model",
        ask_user_heuristic: str = "",
        conversation: Optional[List] = None,
    ) -> None:
        self.llm = llm
        self.model = model
        self.ask_user_heuristic = ask_user_heuristic.strip()
        self.conversation = conversation[-10:] if conversation else []

    @Utils.timeit
    def execute(self, task: str = "") -> str:
        if not self.ask_user_heuristic:
            return ""
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.ASK_USER.format(
                problem_statement=task,
                heuristic=self.ask_user_heuristic,
            ),
        }
        conversation = self.conversation + [system_message]
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=conversation,
            response_format={"type": "json_object"},
        )
        json_str = response.choices[0].message.content
        logger.debug(f"ask user response is: {json_str}")
        try:
            jobject = json.loads(json_str)
            return jobject.get("question", "")
        except json.JSONDecodeError:
            logger.error("Failed to decode the response as JSON for ask user agent.")
            return ""


class GoalAgent(TaskAgent):
    """
    GoalAgent helps to determine problem statement from the conversation between user and SSA
    """

    def __init__(
        self,
        llm: OpenAI = AitomaticLLMConfig.get_aitomatic_llm(),
        model: str = "aitomatic-model",
        conversation: Optional[List] = None,
    ) -> None:
        self.llm = llm
        self.model = model
        self.conversation = conversation[-10:] if conversation else []

    @Utils.timeit
    def execute(self, task: str = "") -> str:
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.PROBLEM_STATEMENT,
        }
        conversation = self.conversation + [system_message]
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=conversation,
            response_format={"type": "json_object"},
        )
        json_str = response.choices[0].message.content
        logger.debug(f"problem statement response is: {json_str}")
        try:
            jobject = json.loads(json_str)
            return jobject.get("problem statement", "")
        except json.JSONDecodeError:
            logger.error("Failed to decode the response as JSON for goal agent.")
            return conversation[-1].get("content", "")
