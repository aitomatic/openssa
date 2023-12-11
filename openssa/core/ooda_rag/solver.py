from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.ooda_rag import Solver
from openssa.core.ooda_rag.heuristic import DefaultOODAHeuristic
from openssa.core.ooda_rag.tools import ReasearchAgentTool
from openssa.utils.llm_config import LLMConfig
from openssa.utils.aitomatic_llm_config import AitomaticLLMConfig


class OodaSSA:
    def __init__(self,
                 task_heuristics,
                 highest_priority_heuristic: str = "",
                 agent_service_context=LLMConfig.get_service_context_llama_2_70b(),
                 llm=AitomaticLLMConfig.get_aitomatic_llm(),
                 rag_llm=LLMConfig.get_llm_llama_2_70b(),
                 embed_model=LLMConfig.get_aito_embeddings(),
                 model='gpt-4-1106-preview'):
        # pylint: disable=too-many-arguments
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

    def activate_resources(self, folder_path: str) -> None:
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
