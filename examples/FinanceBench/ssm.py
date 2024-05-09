from argparse import ArgumentParser
from functools import cache

from openssa import LlamaIndexSSM

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, FbId, Answer, Doc, FB_ID_COL_NAME, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID
from util import enable_batch_qa_and_eval, log_qa_and_update_output_file


@cache
def get_or_create_ssm(doc_name: DocName) -> LlamaIndexSSM | None:
    if dir_path := Doc(name=doc_name).dir_path:
        ssm = LlamaIndexSSM()
        ssm.read_directory(storage_dir=dir_path, re_index=False)
        return ssm

    return None


@enable_batch_qa_and_eval(output_name='SSM')
@log_qa_and_update_output_file(output_name='SSM')
def discuss(fb_id: FbId) -> Answer:
    return (ssm.discuss(QS_BY_FB_ID[fb_id])['content']
            if (ssm := get_or_create_ssm(DOC_NAMES_BY_FB_ID[fb_id]))
            else 'ERROR: doc not found')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()

    discuss(fb_id
            if (fb_id := args.fb_id).startswith(FB_ID_COL_NAME)
            else f'{FB_ID_COL_NAME}_{fb_id}')
