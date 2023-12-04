from dotenv import load_dotenv

load_dotenv()  # it must be called before importing the project modules
from openssa.core.ooda_rag.ooda_rag import Solver
from openssa.core.ooda_rag.heuristic import (
    DefaultOODAHeuristic,
    TaskDecompositionHeuristic,
)
from openssa.core.ooda_rag.tools import ReasearchAgentTool
from openssa.utils.aitomatic_llm_config import AitomaticLLMConfig
from openssa.contrib.custom import CustomSSM


class OodaSSA:
    def __init__(
        self,
        task_heuristics,
        llm=AitomaticLLMConfig.get_llama2_70b(),
        model: str = "llama2",
    ):
        self.llm = llm
        self.solver = Solver(
            task_heuristics=task_heuristics,
            ooda_heuristics=DefaultOODAHeuristic(),
            llm=llm,
            model=model,
        )

    def load(self, folder_path: str) -> None:
        # agent = CustomSSM(llm=self.llm) # TODO fix this to run
        agent = CustomSSM()
        agent.read_directory(folder_path)
        response = agent.discuss("what is mri hahaha")
        print('debug: ', response)
        self.research_documents_tool = ReasearchAgentTool(agent=agent)


    def solve(self, message: str) -> str:
        return self.solver.run(
            message, {"research_documents": self.research_documents_tool}
        )


if __name__ == "__main__":
    heuristic_rules_example = {
        "uncrated picc": [
            "find out the weight of the uncrated PICC",
        ],
        "crated picc": [
            "find out the weight of the crated PICC",
        ],
        "picc": [
            "find out the weight of PICC",
        ],
    }
    task_heuristics = TaskDecompositionHeuristic(heuristic_rules_example)
    ooda_ssa = OodaSSA(task_heuristics)
    print("start reading doc")
    ooda_ssa.load("tests/doc")
    print("finish reading doc")
    print(ooda_ssa.solve("find out the weight of the uncrated PICC"))
    print(ooda_ssa.solve("find out the weight of the crated PICC"))
    print(ooda_ssa.solve("find out the weight of PICC"))
