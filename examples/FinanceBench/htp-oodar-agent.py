from argparse import ArgumentParser
from functools import cache

# pylint: disable=unused-import
from openssa import Agent, HTP, AutoHTPlanner, OodaReasoner, FileResource

# pylint: disable=wrong-import-order
from data_and_knowledge import (DocName, FbId, Answer,
                                FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID, EXPERT_PLAN_MAP, EXPERT_PLAN_TEMPLATES,
                                cache_dir_path)
from util import QAFunc, enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_agent(doc_name: DocName) -> Agent | None:
    return (Agent(planner=AutoHTPlanner(max_depth=2, max_subtasks_per_decomp=3),
                  reasoner=OodaReasoner(),
                  resources={FileResource(path=dir_path)})
            if (dir_path := cache_dir_path(doc_name))
            else None)


@enable_batch_qa_and_eval(output_name='HTP-auto-static---OODAR')
@log_qa_and_update_output_file(output_name='HTP-auto-static---OODAR')
def solve_auto_htp_statically(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], plan=None, dynamic=False)
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


@enable_batch_qa_and_eval(output_name='HTP-auto-dynamic---OODAR')
@log_qa_and_update_output_file(output_name='HTP-auto-dynamic---OODAR')
def solve_auto_htp_dynamically(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], plan=None, dynamic=True)
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


@enable_batch_qa_and_eval(output_name='HTP-expert-static---OODAR')
@log_qa_and_update_output_file(output_name='HTP-expert-static---OODAR')
def solve_expert_htp_statically(fb_id: FbId) -> Answer:
    if agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]):
        problem: str = QS_BY_FB_ID[fb_id]

        if expert_htp_id := EXPERT_PLAN_MAP.get(fb_id):
            htp: HTP = HTP.from_dict(EXPERT_PLAN_TEMPLATES[expert_htp_id])
            htp.task.ask: str = problem
            return agent.solve(problem=problem, plan=htp, dynamic=False)

        return agent.solve(problem=problem, plan=None, dynamic=True)

    return 'ERROR: doc not found'


@enable_batch_qa_and_eval(output_name='HTP-expert-dynamic---OODAR')
@log_qa_and_update_output_file(output_name='HTP-expert-dynamic---OODAR')
def solve_expert_htp_dynamically(fb_id: FbId) -> Answer:  # noqa: ARG001
    raise NotImplementedError('Dynamic execution of given Plan and Planner not yet implemented')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--expert-plan', action='store_true')
    arg_parser.add_argument('--dynamic-exec', action='store_true')
    args = arg_parser.parse_args()

    match (args.expert_plan, args.dynamic_exec):
        case (False, False):
            solve: QAFunc = solve_auto_htp_statically

        case (False, True):
            solve: QAFunc = solve_auto_htp_dynamically

        case (True, False):
            solve: QAFunc = solve_expert_htp_statically

        case (True, True):
            solve: QAFunc = solve_expert_htp_dynamically

    solve(fb_id
          if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
          else f'{FB_ID_COL_NAME}_{fb_id}')
