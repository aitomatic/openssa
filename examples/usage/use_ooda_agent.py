import json
from openssa.core.ssa.agent import Agent
from openssa.core.ooda.heuristic import Heuristic
from openssa.core.ooda.task import Task


def use_ooda_agent(question: str):
    agent = Agent()
    result = agent.solve(question)
    print(f"result: {json.dumps(result.__dict__, indent=4)}")


def use_ooda_agent_with_heuristics(question: str):
    class SolverHeuristic(Heuristic):
        def should_subtask(self, task: Task, llm, history) -> bool:
            if task.goal == "Calculate Total Process Time = (Pulse Time + Purge Time) * Number of Cycles":
                return False
            return True

        def decompose_task(self, task: str, llm, history) -> list:
            return ["Calculate Total Process Time = (Pulse Time + Purge Time) * Number of Cycles"]

    agent = Agent(heuristics=[SolverHeuristic()])
    result = agent.solve(question)
    print(result.__dict__)
