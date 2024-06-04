from argparse import ArgumentParser

# pylint: disable=wrong-import-order
from data_and_knowledge import FbId, Answer, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from rag_default import get_or_create_file_resource
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


@enable_batch_qa_and_eval(output_name='RAG-GPT4-LM')
@log_qa_and_update_output_file(output_name='RAG-GPT4-LM')
def answer(fb_id: FbId) -> Answer:
    return (file_resource.answer(QS_BY_FB_ID[fb_id])
            if (file_resource := get_or_create_file_resource(DOC_NAMES_BY_FB_ID[fb_id], openai_lm_name='gpt-4-1106-preview'))  # noqa: E501
            else 'ERROR: doc not found')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    answer(fb_id
           if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
           else f'{FB_ID_COL_NAME}_{fb_id}')
