from functools import cache
from pathlib import Path

from pandas import DataFrame, read_csv
import requests

from dotenv import load_dotenv
load_dotenv()


METADATA_URL: str = 'https://raw.githubusercontent.com/patronus-ai/financebench/main/financebench_sample_150.csv'

META_DF: DataFrame = read_csv(METADATA_URL)
DOC_NAMES: list[str] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[str, str] = dict(zip(META_DF.doc_name, META_DF.doc_link))
QAS_BY_ID: dict[str, tuple[str, str]] = dict(zip(META_DF.financebench_id, zip(META_DF.question, META_DF.answer)))
QS_BY_ID: dict[str, str] = {i: qa[0] for i, qa in QAS_BY_ID.items()}
QAIDS_BY_DOC_NAME: dict[str, list[str]] = META_DF.groupby('doc_name').apply(lambda df: df.financebench_id.to_list())

LOCAL_CACHE_DIR_PATH: Path = Path(__file__).parent.parent / '.data'
LOCAL_CACHE_DOCS_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = LOCAL_CACHE_DIR_PATH / 'output.csv'


@cache
def cache_dir_path(doc_name: str) -> Path:
    dir_path: Path = LOCAL_CACHE_DOCS_DIR_PATH / doc_name

    if not (file_path := dir_path / doc_name / '.pdf').is_file():
        with open(file=file_path, mode='wb', buffering=-1, encoding=None,
                  errors='strict', newline=None, closefd=True, opener=None) as f:
            f.write(requests.get(url=DOC_LINKS_BY_NAME[doc_name], timeout=9, stream=True).content)

    return dir_path


@cache
def cache_file_path(doc_name: str) -> Path:
    return cache_dir_path(doc_name) / doc_name / '.pdf'
