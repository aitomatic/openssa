from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.ooda_rag import Solver, History
from openssa.core.ooda_rag.heuristic import DefaultOODAHeuristic
from openssa.core.ooda_rag.tools import ReasearchAgentTool
from openssa.core.ooda_rag.builtin_agents import GoalAgent, AgentRole, AskUserAgent
from openssa.utils.llms import OpenAILLM


class OodaSSA:
    def __init__(
        self,
        task_heuristics,
        highest_priority_heuristic: str = "",
        ask_user_heuristic: str = "",
        llm=OpenAILLM.get_gpt_4_1106_preview(),
    ):
        # pylint: disable=too-many-arguments
        self.solver = Solver(
            task_heuristics=task_heuristics,
            ooda_heuristics=DefaultOODAHeuristic(),
            llm=llm,
            highest_priority_heuristic=highest_priority_heuristic,
        )
        self.ask_user_heuristic = ask_user_heuristic
        self.conversation = History()
        self.conversation.add_message("Hi, what can I help you?", AgentRole.ASSISTANT)

    def activate_resources(self, folder_path: str) -> None:
        agent = CustomSSM()

        if folder_path.startswith("s3://"):
            agent.read_s3(folder_path)
        else:
            agent.read_directory(folder_path)

        self.research_documents_tool = ReasearchAgentTool(agent=agent)

    def solve(self, message: str) -> str:
        self.conversation.add_message(message, AgentRole.USER)
        goal_agent = GoalAgent(conversation=self.conversation.get_history())
        problem_statement = goal_agent.execute()
        if not problem_statement:
            return "Sorry, I don't understand your problem."
        ask_user_response = AskUserAgent(
            ask_user_heuristic=self.ask_user_heuristic,
            conversation=self.conversation.get_history(),
        ).execute(problem_statement)
        if ask_user_response:
            return ask_user_response
        assistant_response = self.solver.run(
            problem_statement, {"research_documents": self.research_documents_tool}
        )
        self.conversation.add_message(assistant_response, AgentRole.ASSISTANT)
        return assistant_response
