from openssa.core.ooda_rag.ooda_rag import Solver
from openssa.core.ooda_rag.heuristic import DefaultOODAHeuristic
from openssa.core.ooda_rag.tools import ReasearchAgentTool
from openssa.contrib.custom import CustomSSM


class OodaSSA:
    def __init__(
        self,
        task_heuristics,
        agent_service_context,
        llm,
        rag_llm,
        embed_model,
        model: str,
        highest_priority_heuristic: str = "",
    ):
        self.llm = llm
        self.rag_llm = rag_llm
        self.embed_model = embed_model
        self.agent_service_context = agent_service_context
        self.solver = Solver(
            task_heuristics=task_heuristics,
            ooda_heuristics=DefaultOODAHeuristic(),
            llm=llm,
            model=model,
            highest_priority_heuristic=highest_priority_heuristic,
        )

    def load(self, folder_path: str) -> None:
        agent = CustomSSM(llm=self.rag_llm, embed_model=self.embed_model)

        if folder_path.startswith('s3://'):
            agent.read_s3(folder_path)
        else:
            agent.read_directory(folder_path)

        self.research_documents_tool = ReasearchAgentTool(agent=agent)

    def solve(self, message: str) -> str:
        return self.solver.run(
            message, {"research_documents": self.research_documents_tool}
        )
