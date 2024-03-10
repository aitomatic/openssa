from functools import cache

from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-order,wrong-import-position
from openssa import OodaSSA, TaskDecompositionHeuristic  # noqa: E402

from fb_ssa.data import get_or_create_cached_dir_path  # noqa: E402
from fb_ssa.heuristics import (  # noqa: E402
    THREE_FIN_STATEMENTS_HEURISTICS,
)


@cache
def get_or_create_ooda_ssa(doc_name: str,
                           guiding_heuristics: str = THREE_FIN_STATEMENTS_HEURISTICS) -> OodaSSA:
    print(f'Getting OODA-RAG SSA based on {doc_name}...')

    ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                  highest_priority_heuristic=guiding_heuristics,
                  enable_generative=True)

    ssa.activate_resources(get_or_create_cached_dir_path(doc_name))

    return ssa
