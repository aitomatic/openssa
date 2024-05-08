from argparse import ArgumentParser
from collections import Counter
import base64
from enum import StrEnum
from functools import cache
from pathlib import Path
from typing import TypedDict, Required, NotRequired, Literal

from dotenv import load_dotenv
from pandas import DataFrame, read_csv
import requests
import yaml


load_dotenv()


type DocName = str
type FbId = str
type Question = str
type Answer = str
type ExpertPlanId = str


class Category(StrEnum):
    RETRIEVE: str = '0-RETRIEVE'
    COMPARE: str = '1-COMPARE'
    CALC_CHANGE: str = '2-CALC-CHANGE'
    CALC_COMPLEX: str = '3-CALC-COMPLEX'
    CALC_AND_JUDGE: str = '4-CALC-AND-JUDGE'
    EXPLAIN_FACTORS: str = '5-EXPLAIN-FACTORS'
    OTHER_ADVANCED: str = '6-OTHER-ADVANCED'


NON_BOT_REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


BROKEN_OR_CORRUPT_DOC_NAMES: set[DocName] = {
    'JOHNSON&JOHNSON_2022_10K', 'JOHNSON&JOHNSON_2022Q4_EARNINGS',
    'JOHNSON&JOHNSON_2023_8K_dated-2023-08-30', 'JOHNSON&JOHNSON_2023Q2_EARNINGS',
}


METADATA_URL: str = 'https://raw.githubusercontent.com/patronus-ai/financebench/main/financebench_sample_150.csv'
FB_ID_COL_NAME: str = 'financebench_id'
META_DF: DataFrame = read_csv(METADATA_URL, index_col=FB_ID_COL_NAME)
META_DF: DataFrame = META_DF.loc[~META_DF.doc_name.isin(BROKEN_OR_CORRUPT_DOC_NAMES)]

DOC_NAMES: list[DocName] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[DocName, str] = dict(zip(META_DF.doc_name, META_DF.doc_link))
DOC_NAMES_BY_FB_ID: dict[FbId, DocName] = META_DF.doc_name.to_dict()

FB_IDS: list[FbId] = META_DF.index.to_list()
FB_IDS_BY_DOC_NAME: dict[FbId, list[DocName]] = META_DF.groupby('doc_name').apply(lambda _: _.index.to_list())

QS_BY_FB_ID: dict[FbId, Question] = META_DF.question.to_dict()


LOCAL_CACHE_DIR_PATH: Path = Path(__file__).parent / '.data'
LOCAL_CACHE_DOCS_DIR_PATH: Path = LOCAL_CACHE_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = LOCAL_CACHE_DIR_PATH / 'output.csv'


GROUND_TRUTHS_FILE_PATH = Path(__file__).parent / 'ground-truths.yml'
type GroundTruth = TypedDict('GroundTruth', {'doc': Required[DocName],
                                             'question': Required[Question],
                                             'answer': Required[Answer],
                                             'page(s)': Required[str],
                                             'category': Required[Category],
                                             'correctness': Required[str],
                                             'answer-inadequate': NotRequired[Literal[True]],
                                             'evaluator-unreliable': NotRequired[Literal[True]]})
with open(file=GROUND_TRUTHS_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    GROUND_TRUTHS: dict[FbId, GroundTruth] = yaml.safe_load(stream=f)

CAT_DISTRIB: Counter[Category] = Counter(ground_truth['category'] for ground_truth in GROUND_TRUTHS.values())


EXPERT_PLANS_MAP_FILE_PATH: Path = Path(__file__).parent / 'expert-plans-map.yml'
with open(file=EXPERT_PLANS_MAP_FILE_PATH, encoding='utf-8') as f:
    EXPERT_PLANS_MAP: dict[FbId, ExpertPlanId] = yaml.safe_load(stream=f)

# sanity check Expert Plans Map
cats_of_fb_ids_with_expert_plans: set[Category] = {GROUND_TRUTHS[fb_id]['category'] for fb_id in EXPERT_PLANS_MAP}
assert not cats_of_fb_ids_with_expert_plans & {Category.RETRIEVE, Category.CALC_CHANGE, Category.EXPLAIN_FACTORS}

assert len(EXPERT_PLANS_MAP) == (
    3  # 1-COMPARE: cash-flow-activities
    + CAT_DISTRIB[Category.CALC_COMPLEX] - 3  # 00517, 00882, 00605
    + CAT_DISTRIB[Category.CALC_AND_JUDGE]
    + 2  # 6-OTHER-ADVANCED: capital-intensiveness
    + 3  # 6-OTHER-ADVANCED: fin-svcs-perf
)


EXPERT_PLANS_FILE_PATH: Path = Path(__file__).parent / 'expert-plans.yml'
type Plan = TypedDict('Plan', {'task': Required[str],
                               'sub-plans': Required[list]})
with open(file=EXPERT_PLANS_FILE_PATH, encoding='utf-8') as f:
    EXPERT_PLANS: dict[ExpertPlanId, Plan] = yaml.safe_load(stream=f)


def get_doc(doc_name: DocName) -> requests.Response:
    response: requests.Response = requests.get(
        url=(url := ((base64.b64decode(doc_link.split(sep=q, maxsplit=-1)[-1], altchars=None)
                      .decode(encoding='utf-8', errors='strict'))
                     if (q := '?pdfTarget=') in (doc_link := DOC_LINKS_BY_NAME[doc_name])
                     else doc_link)),
        timeout=60,
        stream=True)

    if response.headers.get('Content-Type') != 'application/pdf':
        response: requests.Response = requests.get(url=url,
                                                   headers=NON_BOT_REQUEST_HEADERS,
                                                   timeout=60,
                                                   stream=True)

    return response


@cache
def cache_dir_path(doc_name: DocName) -> Path | None:
    dir_path: Path = LOCAL_CACHE_DOCS_DIR_PATH / doc_name

    if not (file_path := dir_path / f'{doc_name}.pdf').is_file():
        dir_path.mkdir(parents=True, exist_ok=True)

        response: requests.Response = get_doc(doc_name)

        with open(file=file_path, mode='wb', buffering=-1, encoding=None, newline=None, closefd=True, opener=None) as f:
            f.write(response.content)

    return dir_path


@cache
def cache_file_path(doc_name: DocName) -> Path | None:
    return (dir_path / f'{doc_name}.pdf'
            if (dir_path := cache_dir_path(doc_name))
            else None)


def export_ground_truths():
    with open(file=GROUND_TRUTHS_FILE_PATH,
              mode='w',
              buffering=-1,
              encoding='utf-8',
              errors='strict',
              newline=None,
              closefd=True,
              opener=None) as f:
        yaml.safe_dump(data={fb_id: {'doc': row.doc_name, 'question': row.question, 'answer': row.answer, 'page(s)': row.page_number}  # noqa: E501
                             for fb_id, row in META_DF.iterrows()},
                       stream=f,
                       default_style=None,
                       default_flow_style=False,
                       canonical=None,
                       indent=2,
                       width=80,
                       allow_unicode=True,
                       line_break=None,
                       encoding='utf-8',
                       explicit_start=None,
                       explicit_end=None,
                       version=None,
                       tags=None,
                       sort_keys=False)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('doc_name')
    args = arg_parser.parse_args()

    get_doc(args.doc_name)
