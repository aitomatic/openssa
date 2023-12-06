from openssa.core.ooda_rag.ooda_rag import Solver
from openssa.core.ooda_rag.heuristic import (
    DefaultOODAHeuristic,
    TaskDecompositionHeuristic,
)
from openssa.core.ooda_rag.tools import ReasearchAgentTool
from openssa.utils.aitomatic_llm_config import AitomaticLLMConfig
from openssa.utils.llm_config import LLMConfig
from openssa.contrib.custom import CustomSSM


class OodaSSA:
    def __init__(
        self,
        task_heuristics,
        # llm=AitomaticLLMConfig.get_openai(),
        # model: str = "gpt-3.5-turbo",
        # llm=AitomaticLLMConfig.get_intel_neural_chat_7b(),
        # model="Intel/neural-chat-7b-v3-1",
        llm=AitomaticLLMConfig.get_llama2_70b(),
        model: str = "llama2",
        agent_service_context=LLMConfig.get_service_context_llama_2_70b(),
    ):
        self.llm = llm
        self.agent_service_context = agent_service_context
        self.solver = Solver(
            task_heuristics=task_heuristics,
            ooda_heuristics=DefaultOODAHeuristic(),
            llm=llm,
            model=model,
        )

    def load(self, folder_path: str) -> None:
        agent = CustomSSM(service_context=self.agent_service_context)
        agent.read_directory(folder_path)
        self.research_documents_tool = ReasearchAgentTool(agent=agent)

    def solve(self, message: str) -> str:
        return self.solver.run(
            message, {"research_documents": self.research_documents_tool}
        )


if __name__ == "__main__":
    heuristic_rules_example = {
        "picc": [
            "find out the weight of PICC",
        ],
    }
    task_heuristics = TaskDecompositionHeuristic(heuristic_rules_example)
    ooda_ssa = OodaSSA(task_heuristics)
    print("start reading doc")
    ooda_ssa.load("tests/doc")
    print("finish reading doc")
    print(
        ooda_ssa.solve(
            "if a person can carry 40 kg, how many people needed to carry uncrated PICC"
        )
    )
    # print(ooda_ssa.solve("find out the weight of the crated PICC"))
    # print(ooda_ssa.solve("find out the weight of PICC"))
