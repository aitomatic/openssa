from argparse import ArgumentParser
from functools import cache

from llama_index.llms.openai.base import DEFAULT_OPENAI_MODEL as DEFAULT_LLAMAINDEX_OPENAI_LM

from openssa import FileResource, LMConfig
from openssa.l2.util.lm.openai import LlamaIndexOpenAILM

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_file_resource(doc_name: DocName,
                                llama_index_openai_lm_name: str = DEFAULT_LLAMAINDEX_OPENAI_LM) -> FileResource | None:
    return (FileResource(path=dir_path,
                         lm=LlamaIndexOpenAILM(model=llama_index_openai_lm_name,
                                               temperature=LMConfig.DEFAULT_TEMPERATURE,
                                               max_tokens=None,
                                               additional_kwargs={'seed': LMConfig.DEFAULT_SEED},
                                               max_retries=3, timeout=60, reuse_client=True,
                                               api_key=None, api_base=None, api_version=None,
                                               callback_manager=None, default_headers=None,
                                               http_client=None, async_http_client=None,
                                               system_prompt=None, messages_to_prompt=None, completion_to_prompt=None,
                                               # pydantic_program_mode=...,
                                               output_parser=None))
            if (dir_path := Doc(name=doc_name).dir_path)
            else None)


@enable_batch_qa_and_eval(output_name='RAG-Default')
@log_qa_and_update_output_file(output_name='RAG-Default')
def answer(fb_id: FbId) -> Answer:
    return (file_resource.answer(QS_BY_FB_ID[fb_id])
            if (file_resource := get_or_create_file_resource(doc_name=DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    answer(fb_id
           if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
           else f'{FB_ID_COL_NAME}_{fb_id}')
