from collections.abc import Sequence
from functools import cache
from pathlib import Path

from pandas import DataFrame, read_csv
import requests

from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-position
from openssa.utils.fs import FileSource  # noqa: E402


__all__: Sequence[str] = (
    'META_DF', 'DOC_LINKS_BY_NAME',
    'LOCAL_CACHE_DIR_PATH', 'LOCAL_CACHE_DOCS_DIR_PATH', 'OUTPUT_FILE_PATH',
    'get_or_create_cached_dir_path',
)


FINANCEBENCH_METADATA_URL: str = 'https://raw.githubusercontent.com/patronus-ai/financebench/main/financebench_sample_150.csv'

META_DF: DataFrame = read_csv(FINANCEBENCH_METADATA_URL)
DOC_NAMES: list[str] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[str, str] = dict(zip(META_DF.doc_name, META_DF.doc_link))
QAS_BY_ID: dict[str, tuple[str, str]] = dict(zip(META_DF.financebench_id, zip(META_DF.question, META_DF.answer)))
QS_BY_ID: dict[str, str] = {i: qa[0] for i, qa in QAS_BY_ID.items()}
QAIDS_BY_DOC_NAME: dict[str, list[str]] = META_DF.groupby('doc_name').apply(lambda df: df.financebench_id.to_list())

LOCAL_CACHE_DIR_PATH: Path = Path(__file__).parent.parent / '.FinanceBench'
LOCAL_CACHE_DOCS_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = LOCAL_CACHE_DIR_PATH / 'output.csv'


@cache
def get_or_create_cached_dir_path(doc_name: str) -> str:
    dir_path: Path = LOCAL_CACHE_DOCS_DIR_PATH / doc_name

    doc_path: Path = dir_path / f'{doc_name}.pdf'

    if not (file_src := FileSource(path=str(doc_path))).is_single_file:
        file_src.fs.write_bytes(path=file_src.native_path,
                                value=requests.get(url=DOC_LINKS_BY_NAME[doc_name], stream=True, timeout=9).content)

    return str(dir_path)


@cache
def cached_file_path(doc_name: str) -> str:
    return Path(get_or_create_cached_dir_path(doc_name)) / f'{doc_name}.pdf'
