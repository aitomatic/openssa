from argparse import ArgumentParser
from functools import cache

from data import FbId, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID, cache_dir_path, enable_batch_qa, update_or_create_output_file
from openssa.l2.resource.file import FileResource


@cache
def get_or_create_file_resource(doc_name: str) -> FileResource:
    return FileResource(path=cache_dir_path(doc_name))


@enable_batch_qa
@update_or_create_output_file('RAG-Default')
def answer(fb_id: FbId) -> str:
    return get_or_create_file_resource(DOC_NAMES_BY_FB_ID[fb_id]).answer(QS_BY_FB_ID[fb_id])


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('fb_id')
    args = arg_parser.parse_args()
    print(answer(args.fb_id))
