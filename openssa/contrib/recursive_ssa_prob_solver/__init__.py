# pylint: disable=unused-argument


from openssa import OodaSSA, TaskDecompositionHeuristic  # noqa: E402


class RecursiveOodaSSA:
    def __init__(self, resource_scope: list[str]):
        self.ooda_ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                                enable_generative=True)

    def solve(self, problem: str, max_n_sources: int = 10) -> str:
        solution: str = self.ooda_ssa.solve(problem)
        return solution
