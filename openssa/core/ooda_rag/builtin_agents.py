from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional
import json
from loguru import logger
from openssa.core.ooda_rag.prompts import BuiltInAgentPrompt
from openssa.utils.utils import Utils
from openssa.utils.llms import OpenAILLM, AnLLM


class Persona:
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
        llm: AnLLM = OpenAILLM.get_gpt_4_1106_preview(),
        ask_user_heuristic: str = "",
        conversation: Optional[List] = None,
    ) -> None:
        self.llm = llm
        self.ask_user_heuristic = ask_user_heuristic.strip()
        self.conversation = conversation[-10:-1] if conversation else []

    @Utils.timeit
    def execute(self, task: str = "") -> dict:
        if not self.ask_user_heuristic:
            return ""
        system_message = {
            "role": Persona.SYSTEM,
            "content": BuiltInAgentPrompt.ASK_USER_OODA.format(
                problem_statement=task,
                heuristic=self.ask_user_heuristic,
            ),
        }
        conversation = self.conversation + [system_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "json_object"},
        )
        json_str = response.choices[0].message.content
        logger.debug(f"ask user response is: {json_str}")
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error("Failed to decode the response as JSON for ask user agent.")
            return {}


class CommAgent(TaskAgent):
    """
    CommAgent helps update tone, voice, format and language of the assistant final response
    """

    def __init__(
        self, llm: AnLLM = OpenAILLM(), instruction: str = ""
    ) -> None:
        self.llm = llm
        self.instruction = instruction

    @Utils.timeit
    def execute(self, task: str = "") -> str:
        system_message = {
            "role": Persona.SYSTEM,
            "content": BuiltInAgentPrompt.COMMUNICATION.format(
                instruction=self.instruction, message=task
            ),
        }
        conversation = [system_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "text"},
        )
        return response.choices[0].message.content


class GoalAgent(TaskAgent):
    """
    GoalAgent helps to determine problem statement from the conversation between user and SSA
    """

    def __init__(
        self,
        llm: AnLLM = OpenAILLM.get_gpt_4_1106_preview(),
        conversation: Optional[List] = None,
    ) -> None:
        self.llm = llm
        self.conversation = conversation[-10:] if conversation else []

    @Utils.timeit
    def execute(self, task: str = "") -> str:
        system_message = {
            "role": Persona.SYSTEM,
            "content": BuiltInAgentPrompt.PROBLEM_STATEMENT,
        }
        response = self.llm.call(
            messages=self.conversation + [system_message],
            response_format={"type": "json_object"},
        )
        json_str = response.choices[0].message.content
        logger.debug(f"problem statement response is: {json_str}")
        try:
            return json.loads(json_str).get("problem statement", "")
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON for goal agent.")
            return task


class ContextValidator(TaskAgent):
    """
    ContentValidatingAgent helps to determine whether the content is sufficient to answer the question
    """

    def __init__(
        self,
        llm: AnLLM = OpenAILLM.get_gpt_4_1106_preview(),
        conversation: Optional[List] = None,
        context: Optional[list] = None,
    ) -> None:
        self.llm = llm
        self.conversation = conversation[-10:-1] if conversation else []
        self.context = context

    @Utils.timeit
    def execute(self, task: str = "") -> dict:
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.CONTENT_VALIDATION.format(
                context=self.context, query=task
            ),
        }
        conversation = self.conversation + [system_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "json_object"},
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON for content validation agent.")
            return {}


class AnswerValidator(TaskAgent):
    """
    AnswerValidator helps to determine whether the answer is complete
    """

    def __init__(
        self,
        llm: AnLLM = OpenAILLM.get_gpt_4_1106_preview(),
        answer: str = "",
    ) -> None:
        self.llm = llm
        self.answer = answer

    @Utils.timeit
    def execute(self, task: str = "") -> bool:
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.ANSWER_VALIDATION,
        }
        user_message = {
            "role": "user",
            "content": (
                "Please evaluate the following question and answer pair. "
                "Respond with 'yes' or 'no' only, based on system instruction \n\n"
                f"Question: {task}\n"
                f"Answer: {self.answer}"
            ),
        }
        conversation = [system_message, user_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "text"},
        )
        return response.choices[0].message.content.lower() == "yes"


class SynthesizingAgent(TaskAgent):
    """
    SynthesizeAgent helps to synthesize answer
    """

    def __init__(
        self,
        llm: AnLLM = OpenAILLM.get_gpt_4_1106_preview(),
        conversation: Optional[List] = None,
        context: Optional[list] = None,
    ) -> None:
        self.llm = llm
        self.conversation = conversation[-10:-1] if conversation else []
        self.context = context

    @Utils.timeit
    def execute(self, task: str = "") -> dict:
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.SYNTHESIZE_RESULT.format(
                context=self.context, query=task
            ),
        }
        conversation = self.conversation + [system_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "json_object"},
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON for synthesizing agent.")
            return {}


class OODAPlanAgent(TaskAgent):
    """
    OODAPlanAgent helps to determine the OODA plan from the problem statement
    """

    def __init__(
        self,
        llm: AnLLM = OpenAILLM(),
        conversation: Optional[List] = None,
    ) -> None:
        self.llm = llm
        self.conversation = conversation[-10:] if conversation else []

    @Utils.timeit
    def execute(self, task: str = "") -> dict:
        system_message = {
            "role": "system",
            "content": BuiltInAgentPrompt.GENERATE_OODA_PLAN,
        }
        conversation = self.conversation + [system_message]
        response = self.llm.call(
            messages=conversation,
            response_format={"type": "json_object"},
        )
        json_str = response.choices[0].message.content
        logger.debug(f"OODA plan response is: {json_str}")
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON for OODA plan agent.")
            return {}
