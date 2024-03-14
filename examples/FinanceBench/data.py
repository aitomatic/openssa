from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from pathlib import Path
import sys

from dotenv import load_dotenv
from pandas import DataFrame, read_csv
import requests
from tqdm import tqdm


sys.path.append(str(Path(__file__).parent.parent.parent))
load_dotenv()


type DocName = str
type FbId = str
type Question = str
type Answer = str
type QAFunc = Callable[FbId, Answer]


METADATA_URL: str = 'https://raw.githubusercontent.com/patronus-ai/financebench/main/financebench_sample_150.csv'
META_DF: DataFrame = read_csv(METADATA_URL)

DOC_NAMES: list[DocName] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[str, DocName] = dict(zip(META_DF.doc_name, META_DF.doc_link))
DOC_NAMES_BY_FB_ID: dict[FbId, DocName] = dict(zip(META_DF.financebench_id, META_DF.doc_name))

FB_IDS: list[FbId] = META_DF.financebench_id.to_list()
FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = META_DF.groupby('doc_name').apply(lambda _: _.financebench_id.to_list())

QAS_BY_FB_ID: dict[FbId, tuple[Question, Answer]] = dict(zip(META_DF.financebench_id,
                                                             zip(META_DF.question, META_DF.answer)))
QS_BY_FB_ID: dict[FbId, Question] = {i: q for i, (q, a) in QAS_BY_FB_ID.items()}


LOCAL_CACHE_DIR_PATH: Path = Path(__file__).parent / '.data'
LOCAL_CACHE_DOCS_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = LOCAL_CACHE_DIR_PATH / 'output.csv'


@cache
def cache_dir_path(doc_name: DocName) -> Path:
    dir_path: Path = LOCAL_CACHE_DOCS_DIR_PATH / doc_name

    if not (file_path := dir_path / f'{doc_name}.pdf').is_file():
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(file=file_path, mode='wb', buffering=-1, encoding=None,
                  newline=None, closefd=True, opener=None) as f:
            f.write(requests.get(url=DOC_LINKS_BY_NAME[doc_name], timeout=9, stream=True).content)

    return dir_path


@cache
def cache_file_path(doc_name: DocName) -> Path:
    return cache_dir_path(doc_name) / f'{doc_name}.pdf'


def enable_batch_qa(qa_func: QAFunc) -> QAFunc:
    def decorated_qa_func(fb_id: FbId) -> Answer:
        if 'all' in fb_id.lower():
            for _fb_id in tqdm(FB_IDS):
                qa_func(_fb_id)

            return None

        return qa_func(fb_id)

    return decorated_qa_func


@dataclass
class update_or_create_output_file:  # noqa: N801
    # pylint: disable=invalid-name
    col_name: str

    def __call__(self, qa_func: QAFunc) -> QAFunc:
        def decorated_qa_func(fb_id: FbId) -> Answer:
            answer: str = qa_func(fb_id)

            if OUTPUT_FILE_PATH.is_file():
                output_df: DataFrame = read_csv(OUTPUT_FILE_PATH)

            else:
                output_df: DataFrame = META_DF[['financebench_id', 'doc_name',
                                                'question', 'evidence_text', 'page_number', 'answer']]
                output_df[self.col_name] = None

            output_df.loc[(META_DF.financebench_id == fb_id).idxmax(), self.col_name] = answer

            output_df.to_csv(OUTPUT_FILE_PATH, index=False)

            return answer

        return decorated_qa_func
