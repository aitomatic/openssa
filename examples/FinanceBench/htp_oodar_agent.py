from argparse import ArgumentParser
from functools import cache

from openssa import Agent, ProgramSpace, HTP, HTPlanner, FileResource, LMConfig
from openssa.l2.util.lm.openai import LlamaIndexOpenAILM

# pylint: disable=wrong-import-order
from data_and_knowledge import (DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID,
                                EXPERT_KNOWLEDGE, EXPERT_PROGRAM_SPACE, EXPERT_HTP_COMPANY_KEY, EXPERT_HTP_PERIOD_KEY)
from util import QAFunc, enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_expert_program_space() -> ProgramSpace:
    program_space = ProgramSpace()

    for program_name, htp_dict in EXPERT_PROGRAM_SPACE.items():
        htp = HTP.from_dict(htp_dict)
        program_space.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return program_space


@cache
def get_or_create_agent(doc_name: DocName, expert_knowledge: bool = False, expert_program_space: bool = False,
                        max_depth=2, max_subtasks_per_decomp=4,
                        llama_index_openai_lm_name: str = 'gpt-4o') -> Agent | None:
    # pylint: disable=too-many-arguments
    return (Agent(program_space=get_or_create_expert_program_space() if expert_program_space else ProgramSpace(),
                  programmer=HTPlanner(max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp),
                  knowledge={EXPERT_KNOWLEDGE} if expert_knowledge else None,
                  resources={FileResource(path=dir_path,
                                          lm=LlamaIndexOpenAILM(model=llama_index_openai_lm_name,
                                                                temperature=LMConfig.DEFAULT_TEMPERATURE,
                                                                max_tokens=None,
                                                                additional_kwargs={'seed': LMConfig.DEFAULT_SEED},
                                                                max_retries=3, timeout=60, reuse_client=True,
                                                                api_key=None, api_base=None, api_version=None,
                                                                callback_manager=None, default_headers=None,
                                                                http_client=None, async_http_client=None,
                                                                system_prompt=None, messages_to_prompt=None,
                                                                completion_to_prompt=None,
                                                                # pydantic_program_mode=...,
                                                                output_parser=None))})
            if (dir_path := Doc(name=doc_name).dir_path)
            else None)


@cache
def get_or_create_adaptations(fb_id: FbId) -> dict[str, str]:
    return {EXPERT_HTP_COMPANY_KEY: (doc := Doc(name=DOC_NAMES_BY_FB_ID[fb_id])).company,
            EXPERT_HTP_PERIOD_KEY: doc.period}


@enable_batch_qa_and_eval(output_name='HTP-OODAR')
@log_qa_and_update_output_file(output_name='HTP-OODAR')
def solve(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], **get_or_create_adaptations(fb_id))
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


@enable_batch_qa_and_eval(output_name='HTP-OODAR-wKnowledge')
@log_qa_and_update_output_file(output_name='HTP-OODAR-wKnowledge')
def solve_with_knowledge(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], **get_or_create_adaptations(fb_id))
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True))
            else 'ERROR: doc not found')


@enable_batch_qa_and_eval(output_name='HTP-OODAR-wProgSpace')
@log_qa_and_update_output_file(output_name='HTP-OODAR-wProgSpace')
def solve_with_program_space(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], **get_or_create_adaptations(fb_id))
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id], expert_program_space=True))
            else 'ERROR: doc not found')


@enable_batch_qa_and_eval(output_name='HTP-OODAR-wKnowledge-wProgSpace')
@log_qa_and_update_output_file(output_name='HTP-OODAR-wKnowledge-wProgSpace')
def solve_with_knowledge_and_program_space(fb_id: FbId) -> Answer:
    return (agent.solve(problem=QS_BY_FB_ID[fb_id], **get_or_create_adaptations(fb_id))
            if (agent := get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True, expert_program_space=True))  # noqa: E501
            else 'ERROR: doc not found')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--knowledge', action='store_true')
    arg_parser.add_argument('--prog-space', action='store_true')
    args = arg_parser.parse_args()

    match (args.knowledge, args.prog_space):
        case (False, False):
            solve_func: QAFunc = solve

        case (True, False):
            solve_func: QAFunc = solve_with_knowledge

        case (False, True):
            solve_func: QAFunc = solve_with_program_space

        case (True, True):
            solve_func: QAFunc = solve_with_knowledge_and_program_space

    solve_func(fb_id
               if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
               else f'{FB_ID_COL_NAME}_{fb_id}')
