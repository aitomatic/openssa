from argparse import ArgumentParser
from functools import cache

from openssa import OodaSSA, TaskDecompositionHeuristic

# pylint: disable=wrong-import-order
from data import (DocName, FbId, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID,
                  cache_dir_path, enable_batch_qa, update_or_create_output_file)


THREE_FIN_STATEMENTS_HEURISTICS: str = (
    'pay attention to Balance Sheet, Cash Flow Statement and Profit & Loss (P&L) Statement'
)


@cache
def get_or_create_ooda_ssa(doc_name: DocName,
                           guiding_heuristics: str = THREE_FIN_STATEMENTS_HEURISTICS) -> OodaSSA | None:
    if (dir_path := cache_dir_path(doc_name)):
        ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                      highest_priority_heuristic=guiding_heuristics,
                      enable_generative=True)

        ssa.activate_resources(dir_path)

        return ssa

    return None


@enable_batch_qa
@update_or_create_output_file('OODA')
def solve(fb_id: FbId) -> str:
    return (ooda_ssa.solve(problem=QS_BY_FB_ID[fb_id])
            if (ooda_ssa := get_or_create_ooda_ssa(DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()
    print(solve(args.fb_id))
