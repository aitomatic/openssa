from pathlib import Path

from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.ooda_rag import Solver, History
from openssa.core.ooda_rag.heuristic import (
    Heuristic,
    TaskDecompositionHeuristic,
    HeuristicSet,
)
from openssa.core.ooda_rag.tools import ReasearchAgentTool, Tool
from openssa.core.ooda_rag.builtin_agents import GoalAgent, Persona, AskUserAgent
from openssa.utils.llms import OpenAILLM


class OodaSSA:
    def __init__(
        self,
        task_heuristics: Heuristic = TaskDecompositionHeuristic({}),
        highest_priority_heuristic: str = "",
        ask_user_heuristic: str = "",
        llm=OpenAILLM.get_gpt_4_1106_preview(),
        research_documents_tool: Tool = None,
        enable_generative: bool = False,
    ):
        # pylint: disable=too-many-arguments
        self.heuristic_set = HeuristicSet(
            task_heuristics=task_heuristics,
            highest_priority_heuristic=highest_priority_heuristic,
            ask_user_heuristic=ask_user_heuristic,
        )
        self.solver = Solver(
            heuristic_set=self.heuristic_set,
            llm=llm,
            enable_generative=enable_generative,
        )
        self.conversation = History()
        self.conversation.add_message("Hi, what can I help you?", Persona.ASSISTANT)
        self.research_documents_tool = research_documents_tool

    def activate_resources(self, folder_path: Path | str, re_index: bool = False) -> None:
        agent = CustomSSM()

        if isinstance(folder_path, Path):
            agent.read_directory(folder_path, re_index=re_index)
        elif folder_path.startswith("s3://"):
            agent.read_s3(folder_path)
        else:
            agent.read_directory(folder_path, re_index=re_index)

        self.research_documents_tool = ReasearchAgentTool(agent=agent)

    def get_ask_user_question(self, problem_statement: str) -> str:
        if self.heuristic_set.ask_user_heuristic:
            ask_user_response = AskUserAgent(
                ask_user_heuristic=self.heuristic_set.ask_user_heuristic,
                conversation=self.conversation.get_history(),
            ).execute(problem_statement)
            question = ask_user_response.get("act", "")
            if question:
                ask_user_response["act"] = f"Ask user: {question}"
                print(question)
            return question
        return ""

    def solve(self, task: str) -> str:
        self.conversation.add_message(task, Persona.USER)
        goal_agent = GoalAgent(conversation=self.conversation.get_history())
        problem_statement = goal_agent.execute(task)
        ask_user_question = self.get_ask_user_question(problem_statement)
        if ask_user_question:
            return ask_user_question
        assistant_response = self.solver.run(
            problem_statement, {"research_documents": self.research_documents_tool}
        )
        self.conversation.add_message(
            assistant_response, Persona.ASSISTANT, verbose=False
        )
        return assistant_response
