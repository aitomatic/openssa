from openssa import OodaSSA, TaskDecompositionHeuristic

DOMAIN = "Atomic Layer Deposition (ALD) for Semiconductor"

PROBLEM = (
    "Estimate the ALD process time for 10 cycles, "
    "each with Pulse Time = 15 secs and negligible Inert"
)

EXPERT_HEURISTICS = (
    "Purge Time must be at least as long as Pulse Time, "
    "to clear byproducts between ALD cycles"
)

RESOURCES = "s3://aitomatic-public/KnowledgeBase/Semiconductor/ALD/ALD-Process.txt"


def main():
    ssa = OodaSSA(
        task_heuristics=TaskDecompositionHeuristic({}),
        highest_priority_heuristic=EXPERT_HEURISTICS,
        ask_user_heuristic="",
    )

    ssa.activate_resources(RESOURCES)
    solution = ssa.solve(PROBLEM)
    print(solution)


if __name__ == "__main__":
    main()
