from argparse import ArgumentParser
from functools import cache

from openssa import DANA, ProgramStore, HTP, HTPlanner, FileResource, LMConfig
from openssa.core.util.lm.huggingface import HuggingFaceLM
from openssa.core.util.lm.openai import OpenAILM, default_llama_index_openai_lm

# pylint: disable=wrong-import-order,wrong-import-position
from data_and_knowledge import (DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID,
                                EXPERT_KNOWLEDGE, EXPERT_PROGRAMS, EXPERT_HTP_COMPANY_KEY, EXPERT_HTP_PERIOD_KEY)
from util import QAFunc, enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_main_lm(use_llama: bool = False):
    return (HuggingFaceLM if use_llama else OpenAILM).from_defaults()


@cache
def get_or_create_expert_program_store(use_llama: bool = False) -> ProgramStore:
    program_store = ProgramStore(lm=get_main_lm(use_llama=use_llama))

    for program_name, htp_dict in EXPERT_PROGRAMS.items():
        htp = HTP.from_dict(htp_dict)
        program_store.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return program_store


@cache
def get_or_create_agent(doc_name: DocName, expert_knowledge: bool = False, expert_programs: bool = False,
                        max_depth=3, max_subtasks_per_decomp=6,
                        use_llama: bool = False,
                        llama_index_openai_lm_name: str = LMConfig.OPENAI_DEFAULT_MODEL) -> DANA:
    # pylint: disable=too-many-arguments
    return DANA(knowledge={EXPERT_KNOWLEDGE} if expert_knowledge else None,

                program_store=(get_or_create_expert_program_store(use_llama=use_llama)
                               if expert_programs
                               else ProgramStore()),

                programmer=HTPlanner(lm=get_main_lm(use_llama=use_llama),
                                     max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp),

                resources={FileResource(path=Doc(name=doc_name).dir_path,
                                        lm=default_llama_index_openai_lm(llama_index_openai_lm_name))})


@cache
def get_or_create_adaptations(doc_name: DocName) -> dict[str, str]:
    return {EXPERT_HTP_COMPANY_KEY: (doc := Doc(name=doc_name)).company, EXPERT_HTP_PERIOD_KEY: doc.period}


@enable_batch_qa_and_eval(output_name='DANA')
@log_qa_and_update_output_file(output_name='DANA')
def solve(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id]).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wKnowledge')
@log_qa_and_update_output_file(output_name='DANA-wKnowledge')
def solve_with_knowledge(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wProgStore')
@log_qa_and_update_output_file(output_name='DANA-wProgStore')
def solve_with_program_store(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id], expert_programs=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wKnowledge-wProgStore')
@log_qa_and_update_output_file(output_name='DANA-wKnowledge-wProgStore')
def solve_with_knowledge_and_program_store(fb_id: FbId) -> Answer:
    return get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True, expert_programs=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wLlama')
@log_qa_and_update_output_file(output_name='DANA-wLlama')
def solve_with_llama(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id], use_llama=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wKnowledge-wLlama')
@log_qa_and_update_output_file(output_name='DANA-wKnowledge-wLlama')
def solve_with_knowledge_with_llama(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True, use_llama=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wProgStore-wLlama')
@log_qa_and_update_output_file(output_name='DANA-wProgStore-wLlama')
def solve_with_program_store_with_llama(fb_id: FbId) -> Answer:
    return get_or_create_agent(doc_name=DOC_NAMES_BY_FB_ID[fb_id], expert_programs=True, use_llama=True).solve(
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


@enable_batch_qa_and_eval(output_name='DANA-wKnowledge-wProgStore-wLlama')
@log_qa_and_update_output_file(output_name='DANA-wKnowledge-wProgStore-wLlama')
def solve_with_knowledge_and_program_store_with_llama(fb_id: FbId) -> Answer:
    return get_or_create_agent(DOC_NAMES_BY_FB_ID[fb_id], expert_knowledge=True, expert_programs=True, use_llama=True).solve(  # noqa: E501
        problem=QS_BY_FB_ID[fb_id],
        adaptations_from_known_programs=get_or_create_adaptations(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--from-id', action='store_true')
    arg_parser.add_argument('--knowledge', action='store_true')
    arg_parser.add_argument('--prog-store', action='store_true')
    arg_parser.add_argument('--llama', action='store_true')
    args = arg_parser.parse_args()

    match (args.knowledge, args.prog_store, args.llama):
        case (False, False, False):
            solve_func: QAFunc = solve

        case (True, False, False):
            solve_func: QAFunc = solve_with_knowledge

        case (False, True, False):
            solve_func: QAFunc = solve_with_program_store

        case (True, True, False):
            solve_func: QAFunc = solve_with_knowledge_and_program_store

        case (False, False, True):
            solve_func: QAFunc = solve_with_llama

        case (True, False, True):
            solve_func: QAFunc = solve_with_knowledge_with_llama

        case (False, True, True):
            solve_func: QAFunc = solve_with_program_store_with_llama

        case (True, True, True):
            solve_func: QAFunc = solve_with_knowledge_and_program_store_with_llama

    if not (fb_id := args.fb_id).startswith(FB_ID_COL_NAME):
        fb_id: FbId = f'{FB_ID_COL_NAME}_{fb_id}'

    solve_func(f'from:{fb_id}' if args.from_id else fb_id)
