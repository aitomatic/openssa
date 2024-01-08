from openssa.core.ssa.agent import Agent

def solve(objective):
    # Create an instance of the Agent class
    agent = Agent()

    # Use the agent as a client to solve a problem
    result = agent.solve(objective)

    print(f"Result: {result}")


if __name__ == '__main__':
    OBJECTIVE = ("I want to estimate the ALD process time for 10 cycles, "
                 "each with Pulse Time = 15 secs, Purge Time = 10 secs "
                 "and negligible Inert")
    solve(OBJECTIVE)
