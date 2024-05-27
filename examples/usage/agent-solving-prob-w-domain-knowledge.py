from openssa import (
    Agent,
    # plus informational resources
)


agent = Agent(
    knowledge={...},  # set of knowledge stored in strings
    resources={...},  # set of informational resources
)

agent.solve(problem=...)
