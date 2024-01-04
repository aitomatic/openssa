# pylint: disable=invalid-name


from openssa.core.ooda_rag.heuristic import (
    TaskDecompositionHeuristic,
)
from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.solver import OodaSSA

FOLDER = "/Users/sang/WorkSpace/Aitomatic/openssa-ald"
PROBLEM = """I want to estimate the ALD process time for 10 cycles, each with Pulse Time = 15 secs, Purge Time = 10 secs and negligible Inert"""


def use_custom_ssm():
    agent = CustomSSM()
    agent.read_directory(FOLDER)
    print("finish reading doc")
    res = agent.discuss(PROBLEM)
    print(res)


def use_ooda():
    task_heuristics = TaskDecompositionHeuristic({})
    highest_priority_heuristic = (
        "The Purge Time must be at least as long as the Precursor Pulse Time "
        "to ensure that all excess precursor and reaction byproducts are removed "
        "from the chamber before the next cycle begins."
    )
    ooda_ssa = OodaSSA(
        task_heuristics=task_heuristics,
        highest_priority_heuristic=highest_priority_heuristic,
    )
    ooda_ssa.activate_resources(FOLDER)
    print("finish reading doc")
    res = ooda_ssa.solve(PROBLEM)
    print(res)


if __name__ == "__main__":
    # use_custom_ssm()
    use_ooda()
