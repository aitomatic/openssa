from openssa import (
    Agent,
    AutoHTPlanner,
    OodaReasoner,
    # plus informational resources
)


agent = Agent(
    planner=AutoHTPlanner(max_depth=2, max_subtasks_per_decomp=3),
    reasoner=OodaReasoner(),
    knowledge={...},  # set of knowledge stored in strings
    resources={...},  # set of informational resources
)

agent.solve(
    problem=...,
    plan=...,  # optional user-provided/expert-guided plan
    dynamic=...,  # True: execute with as-needed task decomposition; False: execute literally per plan as-is
)
