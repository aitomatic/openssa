from functools import cache
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pandas import DataFrame, read_csv
import requests


load_dotenv()


type DocName = str
type FbId = str
type Question = str
type Answer = str


BROKEN_OR_CORRUPT_DOC_NAMES: set[DocName] = {
    'ADOBE_2015_10K', 'ADOBE_2016_10K', 'ADOBE_2017_10K', 'ADOBE_2022_10K',
    'JOHNSON&JOHNSON_2022_10K', 'JOHNSON&JOHNSON_2022Q4_EARNINGS',
    'JOHNSON&JOHNSON_2023_8K_dated-2023-08-30', 'JOHNSON&JOHNSON_2023Q2_EARNINGS',
    'MGMRESORTS_2022Q4_EARNINGS',
}


METADATA_URL: str = 'https://raw.githubusercontent.com/patronus-ai/financebench/main/financebench_sample_150.csv'
FB_ID_COL_NAME: str = 'financebench_id'
META_DF: DataFrame = read_csv(METADATA_URL, index_col=FB_ID_COL_NAME)
META_DF: DataFrame = META_DF.loc[~META_DF.doc_name.isin(BROKEN_OR_CORRUPT_DOC_NAMES)]

DOC_NAMES: list[DocName] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[str, DocName] = dict(zip(META_DF.doc_name, META_DF.doc_link))
DOC_NAMES_BY_FB_ID: dict[FbId, DocName] = META_DF.doc_name.to_dict()

FB_IDS: list[FbId] = META_DF.index.to_list()
FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = META_DF.groupby('doc_name').apply(lambda _: _.index.to_list())

QS_BY_FB_ID: dict[FbId, Question] = META_DF.question.to_dict()


LOCAL_CACHE_DIR_PATH: Path = Path(__file__).parent / '.data'
LOCAL_CACHE_DOCS_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = LOCAL_CACHE_DIR_PATH / 'output.csv'


@cache
def cache_dir_path(doc_name: DocName) -> Path | None:
    dir_path: Path = LOCAL_CACHE_DOCS_DIR_PATH / doc_name

    if not (file_path := dir_path / f'{doc_name}.pdf').is_file():
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(file=file_path, mode='wb', buffering=-1, encoding=None,
                  newline=None, closefd=True, opener=None) as f:
            try:
                f.write(requests.get(url=DOC_LINKS_BY_NAME[doc_name], timeout=30, stream=True).content)

            except requests.exceptions.ConnectionError as err:
                logger.error(f'*** {doc_name} ***\n{err}')
                return None

    return dir_path


@cache
def cache_file_path(doc_name: DocName) -> Path | None:
    return (dir_path / f'{doc_name}.pdf'
            if (dir_path := cache_dir_path(doc_name))
            else None)
