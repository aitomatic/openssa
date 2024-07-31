from argparse import ArgumentParser
from functools import cache

from openssa import FileResource, LMConfig
from openssa.core.util.lm.openai import default_llama_index_openai_lm

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_file_resource(doc_name: DocName,
                                llama_index_openai_lm_name: str = LMConfig.DEFAULT_SMALL_OPENAI_MODEL) -> FileResource:
    return FileResource(path=Doc(name=doc_name).dir_path,
                        lm=default_llama_index_openai_lm(llama_index_openai_lm_name))


@enable_batch_qa_and_eval(output_name='RAG-Default')
@log_qa_and_update_output_file(output_name='RAG-Default')
def answer(fb_id: FbId) -> Answer:
    return get_or_create_file_resource(doc_name=DOC_NAMES_BY_FB_ID[fb_id]).answer(question=QS_BY_FB_ID[fb_id])


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    answer(fb_id
           if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
           else f'{FB_ID_COL_NAME}_{fb_id}')
