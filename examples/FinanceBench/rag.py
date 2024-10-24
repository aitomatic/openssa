from argparse import ArgumentParser
from functools import cache

from llama_index.llms.openai.base import DEFAULT_OPENAI_MODEL

from openssa import FileResource, LMConfig
from openssa.core.util.lm.openai import default_llama_index_openai_embed_model, default_llama_index_openai_lm

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_file_resource(doc_name: DocName,
                                llama_index_openai_lm_name: str = LMConfig.OPENAI_DEFAULT_SMALL_MODEL) -> FileResource:
    return FileResource(path=Doc(name=doc_name).dir_path,
                        embed_model=default_llama_index_openai_embed_model(),
                        lm=default_llama_index_openai_lm(llama_index_openai_lm_name))


@enable_batch_qa_and_eval(output_name=f'RAG-{DEFAULT_OPENAI_MODEL}-LM')
@log_qa_and_update_output_file(output_name=f'RAG-{DEFAULT_OPENAI_MODEL}-LM')
def answer_with_default_lm(fb_id: FbId) -> Answer:
    return get_or_create_file_resource(
        doc_name=DOC_NAMES_BY_FB_ID[fb_id],
        llama_index_openai_lm_name=DEFAULT_OPENAI_MODEL).answer(question=QS_BY_FB_ID[fb_id])


@enable_batch_qa_and_eval(output_name=f'RAG-{LMConfig.OPENAI_DEFAULT_SMALL_MODEL}-LM')
@log_qa_and_update_output_file(output_name=f'RAG-{LMConfig.OPENAI_DEFAULT_SMALL_MODEL}-LM')
def answer_with_gpt4o_lm(fb_id: FbId) -> Answer:
    return get_or_create_file_resource(
        doc_name=DOC_NAMES_BY_FB_ID[fb_id],
        llama_index_openai_lm_name=LMConfig.OPENAI_DEFAULT_SMALL_MODEL).answer(question=QS_BY_FB_ID[fb_id])


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    arg_parser.add_argument('--from-id', action='store_true')
    arg_parser.add_argument('--gpt4o', action='store_true')
    args = arg_parser.parse_args()

    if not (fb_id := args.fb_id).startswith(FB_ID_COL_NAME):
        fb_id: FbId = f'{FB_ID_COL_NAME}_{fb_id}'

    (answer_with_gpt4o_lm if args.gpt4o else answer_with_default_lm)(f'from:{fb_id}' if args.from_id else fb_id)
