from argparse import ArgumentParser
from functools import cache

from openssa import Agent, HTP, AutoHTPlanner, OodaReasoner, FileResource

# pylint: disable=wrong-import-order
from data import DocName, FbId, Answer, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID, cache_dir_path
from util import enable_batch_qa, log_qa_and_update_output_file


@cache
def get_or_create_agent(doc_name: DocName) -> Agent | None:
    return (Agent(planner=AutoHTPlanner(max_depth=2, max_subtasks_per_decomp=3),
                  reasoner=OodaReasoner(),
                  resources={FileResource(path=dir_path)})
            if (dir_path := cache_dir_path(doc_name))
            else None)


@enable_batch_qa
@log_qa_and_update_output_file(output_name='HTP-auto-dynamic---OODAR')
def solve_automatically_dynamically(fb_id: FbId) -> Answer:
    if agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]):
        try:
            return agent.solve(QS_BY_FB_ID[fb_id])

        except Exception as err:  # pylint: disable=broad-exception-caught
            return f'ERROR: {err}'

    return 'ERROR: doc not found'


@enable_batch_qa
@log_qa_and_update_output_file(output_name='HTP-auto-static---OODAR')
def solve_automatically_statically(fb_id: FbId) -> Answer:
    if agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]):
        try:
            return agent.solve(QS_BY_FB_ID[fb_id], dynamic=False)

        except Exception as err:  # pylint: disable=broad-exception-caught
            return f'ERROR: {err}'

    return 'ERROR: doc not found'


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--static', action='store_true')
    args = arg_parser.parse_args()

    solve = (solve_automatically_statically
             if args.static
             else solve_automatically_dynamically)

    solve(fb_id
          if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
          else f'{FB_ID_COL_NAME}_{fb_id}')
