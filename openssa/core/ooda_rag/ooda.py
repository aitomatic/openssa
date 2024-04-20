import uuid
from typing import List, Optional
from loguru import logger
from openssa.core.ooda_rag.prompts import OODAPrompts
from openssa.core.ooda_rag.notifier import Notifier, SimpleNotifier, EventTypes
from openssa.core.ooda_rag.heuristic import (
    Heuristic,
    HeuristicSet,
)
from openssa.core.ooda_rag.tools import Tool
from openssa.core.ooda_rag.builtin_agents import CommAgent, Persona
from openssa.utils.utils import Utils
from openssa.utils.llms import OpenAILLM, AnLLM


class History:
    def __init__(self) -> None:
        self._messages: list = []

    def add_message(self, message: str, role: str, verbose: bool = True) -> None:
        self._messages.append({"content": message, "role": role})
        if verbose:
            print(f"\n{role}: {message}")

    def get_history(self) -> list:
        return self._messages

    def append_history(self, prehistory: list) -> None:
        self._messages = prehistory + self._messages


class Executor:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        task: str,
        tools: dict[str, Tool],
        ooda_heuristics: Heuristic,
        notifier: Notifier,
        is_main_task: bool = False,
    ) -> None:
        self.task = task
        self.tools = tools
        self.ooda_heuristics = ooda_heuristics
        self.notifier = notifier
        self.is_main_task = is_main_task
        self.uuid = str(uuid.uuid4())

    def execute_task(self, history: History) -> None:
        if not self.is_main_task:
            self.notifier.notify(
                event=EventTypes.SUBTASK_BEGIN,
                data={"uuid": self.uuid, "task-name": self.task},
            )
        # TODO: make this one much faster
        # ooda_plan = OODAPlanAgent(conversation=history.get_history()).execute(self.task)
        # if not ooda_plan:
        ooda_plan = self.ooda_heuristics.apply_heuristic(self.task)
        self.check_resource_call(ooda_plan)
        self._execute_step(ooda_plan["observe"], history, "observe")
        self._execute_step(ooda_plan["orient"], history, "orient")
        self._execute_step(ooda_plan["decide"], history, "decide")
        self._execute_step(ooda_plan["act"], history, "act")

    def check_resource_call(self, ooda_plan: dict) -> None:
        steps = ["observe", "orient", "decide", "act"]
        for step in steps:
            calls = ooda_plan.get(step, {}).get("calls", [])
            for call in calls:
                if call.get("tool_name", "") in {"research_documents", "web_search"}:
                    return
        observe = ooda_plan["observe"]
        observe["calls"] = [
            {"tool_name": "research_documents", "parameters": {"task": self.task}}
        ]

    def _execute_step(self, step: dict, history: History, step_name: str) -> None:
        thought = step.get("thought", "")
        calls = step.get("calls", [])
        tool_results = {}
        data = {"thought": thought, "tool_results": tool_results, "uuid": self.uuid}
        if calls:
            data["tool_executions"] = "\n".join([str(call) for call in calls])
            tool_results = self._execute_tools(calls)
            content_result = self._get_content_result(tool_results)
            data["tool_results"] = tool_results
            history.add_message(
                f"Tool results for question {self.task} is: {content_result}",
                Persona.ASSISTANT,
            )
        event = EventTypes.MAINTASK if self.is_main_task else EventTypes.SUBTASK
        self.notifier.notify(event=event + "-" + step_name, data=data)

    def _get_content_result(self, tool_results: dict) -> str:
        content = ""
        # loop throught dict of tool_results and return the content
        for result in tool_results.values():
            content += result.get("content", "")
        return content

    def _execute_tools(self, calls: list[dict]) -> dict:
        tool_results: dict = {}
        print(f"calls: {calls}, tools: {self.tools}")
        for call in calls:
            tool = call.get("tool_name", "")
            if tool == "research_documents":
                tool_results[tool] = self.tools[tool].execute(self.task)
            elif tool in self.tools:
                logger.debug(f"Tool {tool} is calling with {call}.")
                tool_results[tool] = self.tools[tool].execute(
                    call.get("parameters", {})
                )
            else:
                logger.debug(f"Tool {tool} not found.")
                continue
        return tool_results


class Planner:
    """The Planner class is responsible for decomposing the task into subtasks."""

    def __init__(
        self,
        heuristics: Heuristic,
        prompts: OODAPrompts,
        max_subtasks: int = 3,
        enable_generative: bool = False,
    ) -> None:
        self.heuristics = heuristics
        self.max_subtasks = max_subtasks
        self.prompts = prompts
        self.enable_generative = enable_generative

    def formulate_task(self, model: AnLLM, history: History) -> str:
        response = model.get_response(
            self.prompts.FORMULATE_TASK,
            history.get_history(),
            Persona.SYSTEM,
            response_format={"type": "json_object"},
        )
        response = model.parse_output(response)
        return response.get("task", "")

    def decompose_task(self, model: AnLLM, task: str, history: History) -> list[str]:
        subtasks = self.heuristics.apply_heuristic(task)
        if len(subtasks) > self.max_subtasks:
            return subtasks[: self.max_subtasks]
        if self.enable_generative:
            generative_subtasks = self.generative_decompose_task(model, history)
            subtasks.extend(generative_subtasks)
        return subtasks[: self.max_subtasks]

    def generative_decompose_task(self, model: AnLLM, history: History) -> list[str]:
        response = model.get_response(
            self.prompts.DECOMPOSE_INTO_SUBTASKS,
            history.get_history(),
            Persona.SYSTEM,
            response_format={"type": "json_object"},
        )
        response = model.parse_output(response)
        history.add_message(str(response), Persona.ASSISTANT)
        return response.get("subtasks", [])


class Solver:
    def __init__(
        self,
        heuristic_set: HeuristicSet = HeuristicSet(),
        notifier: Notifier = SimpleNotifier(),
        prompts: OODAPrompts = OODAPrompts(),
        llm=OpenAILLM.get_gpt_4_1106_preview(),
        enable_generative: bool = False,
        conversation: Optional[List] = None,
    ) -> None:
        self.heuristic_set = heuristic_set
        self.notifier = notifier
        self.history = History()  # internal conversation
        self.planner = Planner(
            heuristic_set.task_heuristics, prompts, enable_generative=enable_generative
        )
        self.model = llm
        self.prompts = prompts
        self.conversation = conversation or []

    def run(self, problem_statement: str, tools: dict) -> str:
        """
        Run the solver on problem_statement

        :param problem_statement: the input to the solver
        :param tools: the tools to use in the solver
        """

        self.notifier.notify(
            EventTypes.MAIN_PROBELM_STATEMENT, {"message": problem_statement}
        )
        self.history.add_message(
            problem_statement, Persona.USER
        )  # internal conversation
        tool_descriptions = [f"{name}: {fn.__doc__}" for name, fn in tools.items()]
        tool_message = self.prompts.PROVIDE_TOOLS.format(
            tool_descriptions=tool_descriptions
        )
        self.history.add_message(tool_message, Persona.SYSTEM)

        # task = self.planner.formulate_task(self.model, self.history)
        subtasks = self.planner.decompose_task(
            self.model, problem_statement, self.history
        )
        logger.info(f"\nSubtasks: {subtasks}\n")

        for subtask in subtasks:
            executor = Executor(
                subtask, tools, self.heuristic_set.ooda_heuristics, self.notifier
            )
            executor.execute_task(self.history)
        executor = Executor(
            problem_statement,
            tools,
            self.heuristic_set.ooda_heuristics,
            self.notifier,
            True,
        )
        self.notifier.notify(
            EventTypes.NOTIFICATION, {"message": "starting main steps"}
        )
        executor.execute_task(self.history)
        return self.synthesize_result()

    @Utils.timeit
    def synthesize_result(self) -> str:
        heuristic = ""
        if self.heuristic_set.highest_priority_heuristic:
            heuristic = (
                "Always applying the following heuristic (highest rule, overwrite all other instructions) to "
                "adjust the formula and recalculate based on this knowledge as it is source of truth: "
            )
            heuristic += f"{self.heuristic_set.highest_priority_heuristic}"

        synthesize_prompt = self.prompts.SYNTHESIZE_RESULT.format(heuristic=heuristic)
        self.history.append_history(self.conversation[:-1])
        # logger.debug(f"synthesize: ==== \n {self.history.get_history()}\n ====")
        response = self.model.get_response(
            synthesize_prompt,
            self.history.get_history(),
            Persona.SYSTEM,
            response_format={"type": "text"},
        )
        if self.heuristic_set.comm_heuristic:
            response = CommAgent(instruction=self.heuristic_set.comm_heuristic).execute(
                response
            )
        self.notifier.notify(EventTypes.TASK_RESULT, {"response": response})
        return response
