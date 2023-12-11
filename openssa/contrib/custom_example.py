from openssa.core.ooda_rag.heuristic import (
    TaskDecompositionHeuristic,
)
from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.solver import OodaSSA
from openssa.utils.llm_config import LLMConfig
from openssa.utils.aitomatic_llm_config import AitomaticLLMConfig

FOLDER = "/Users/sang/WorkSpace/Aitomatic/openssa-ald"
PROBLEM = """I want to estimate the ALD process time for 10 cycles, each with Pulse Time = 15 secs, Purge Time = 10 secs and negligible Inert"""


def use_custom_ssm():
    service_context = LLMConfig.get_service_context_llama_2_70b()
    agent = CustomSSM(
        service_context=service_context,
    )
    agent.read_directory(FOLDER)
    print("finish reading doc")
    res = agent.discuss(PROBLEM)
    print(res)


def use_ooda():
    task_heuristics = TaskDecompositionHeuristic({})
    highest_priority_heuristic = ('The Purge Time must be at least as long as the Precursor Pulse Time '
                                  'to ensure that all excess precursor and reaction byproducts are removed '
                                  'from the chamber before the next cycle begins.')
    ooda_ssa = OodaSSA(
        task_heuristics=task_heuristics,
        highest_priority_heuristic=highest_priority_heuristic,
        agent_service_context=LLMConfig.get_service_context_llama_2_70b(),
        llm=AitomaticLLMConfig.get_aitomatic_llm(),
        rag_llm = LLMConfig.get_llm_llama_2_70b(),
        embed_model=LLMConfig.get_aito_embeddings(),
        model="gpt-4-1106-preview",
    )
    ooda_ssa.load(FOLDER)
    print("finish reading doc")
    res = ooda_ssa.solve(PROBLEM)
    print(res)


if __name__ == "__main__":
    # use_custom_ssm()
    use_ooda()
