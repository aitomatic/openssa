import json
from openssa.core.ssa.agent import Agent


def use_ooda_agent(question: str):
    # create the agent
    agent = Agent()
    result = agent.solve(question)
    print(f"result: {json.dumps(result.__dict__, indent=4)}")
