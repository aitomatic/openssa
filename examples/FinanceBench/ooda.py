from argparse import ArgumentParser
from functools import cache

from openssa import OodaSSA, TaskDecompositionHeuristic

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


THREE_FIN_STATEMENTS_HEURISTICS: str = (
    'pay attention to Balance Sheet, Cash Flow Statement and Profit & Loss (P&L) Statement'
)


@cache
def get_or_create_ooda_ssa(doc_name: DocName,
                           guiding_heuristics: str = THREE_FIN_STATEMENTS_HEURISTICS) -> OodaSSA | None:
    if (dir_path := Doc(name=doc_name).dir_path):
        ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                      highest_priority_heuristic=guiding_heuristics,
                      enable_generative=True)

        ssa.activate_resources(dir_path)

        return ssa

    return None


@enable_batch_qa_and_eval(output_name='OODA')
@log_qa_and_update_output_file(output_name='OODA')
def solve(fb_id: FbId) -> Answer:
    if ooda_ssa := get_or_create_ooda_ssa(DOC_NAMES_BY_FB_ID[fb_id]):
        try:
            return ooda_ssa.solve(QS_BY_FB_ID[fb_id])

        except Exception as err:  # pylint: disable=broad-exception-caught
            return f'ERROR: {err}'

    return 'ERROR: doc not found'


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    solve(fb_id
          if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
          else f'{FB_ID_COL_NAME}_{fb_id}')
