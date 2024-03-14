from functools import cache

from openssa import OodaSSA, TaskDecompositionHeuristic

# pylint: disable=wrong-import-order
from data import cache_dir_path


THREE_FIN_STATEMENTS_HEURISTICS: str = (
    'pay attention to Balance Sheet, Cash Flow Statement and Profit & Loss (P&L) Statement'
)


@cache
def get_or_create_ooda_ssa(doc_name: str,
                           guiding_heuristics: str = THREE_FIN_STATEMENTS_HEURISTICS) -> OodaSSA:
    ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                  highest_priority_heuristic=guiding_heuristics,
                  enable_generative=True)

    ssa.activate_resources(cache_dir_path(doc_name))

    return ssa
