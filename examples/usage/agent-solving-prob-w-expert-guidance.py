from openssa import (
    Agent,
    HTP,
    # plus informational resources
)


agent = Agent(
    resources={...},  # set of informational resources
)

# TODO: allow users to create such expert plans straight from natural language (but only if reliably)
expert_plan = HTP.from_dict(
    {
        'task': ...,
        'sub-plans': [
            {
                'task': '...',
                'sub-plans': [
                    {
                        'task': '...'
                    },
                    {
                        'task': '...'
                    },
                ]
            },
            {
                'task': '...'
            },
            {
                'task': '...'
            },
        ]
    }
)

agent.solve(
    problem=...,
    plan=expert_plan,  # user-provided/expert-guided plan
)
