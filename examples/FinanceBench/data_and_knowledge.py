from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import base64
from enum import StrEnum
from functools import cached_property
from pathlib import Path
from typing import TypedDict, Required, NotRequired, Literal, TYPE_CHECKING

from dotenv import load_dotenv
from pandas import DataFrame, read_json, read_csv
import requests
import yaml

if TYPE_CHECKING:
    from openssa.core.planning.hierarchical.plan import HTPDict


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


type GroundTruth = TypedDict('GroundTruth', {'sector': Required[str],

                                             'company': Required[str],
                                             'period': Required[int],
                                             'doc-type': Required[str],
                                             'doc': Required[DocName],

                                             'question-type': Required[str],
                                             'question-reasoning': Required[str],
                                             'domain-question-num': Required[str | None],
                                             'question': Required[Question],

                                             'answer': Required[Answer],
                                             'justification': Required[str],
                                             'page(s)-0based': Required[int],
                                             'page(s)': Required[str],

                                             'category': Required[Category],
                                             'correctness': Required[str],
                                             'answer-inadequate': NotRequired[Literal[True]],
                                             'evaluator-unreliable': NotRequired[Literal[True]]},
                             total=False)


type RAGGroundTruths = TypedDict('RAGGroundTruths', {'defs': Required[dict[str, str]],
                                                     'ground-truths': Required[dict[str,  # doc
                                                                                    dict[str,  # statement
                                                                                         dict[str,  # line item
                                                                                              dict[int | str,  # period
                                                                                                   str  # ground truth
                                                                                                   ]]]]]})


NON_BOT_REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


REPO_RAW_CONTENT_URL_PREFIX: str = 'https://raw.githubusercontent.com/patronus-ai/financebench'
DOC_INFO_URL: str = f'{REPO_RAW_CONTENT_URL_PREFIX}/main/data/financebench_document_information.jsonl'
METADATA_JSONL_URL: str = f'{REPO_RAW_CONTENT_URL_PREFIX}/main/data/financebench_open_source.jsonl'
METADATA_CSV_URL: str = f'{REPO_RAW_CONTENT_URL_PREFIX}/641ae9ece2cae93c671cf59c2d53742b51c7f1aa/financebench_sample_150.csv'

FB_ID_COL_NAME: str = 'financebench_id'

META_DF: DataFrame = (read_json(METADATA_JSONL_URL,
                                orient='records', typ='frame',
                                dtype=True, convert_axes=True,
                                convert_dates=True, keep_default_dates=True,
                                precise_float=False, date_unit=None,
                                encoding='utf-8', encoding_errors='strict',
                                lines=True, chunksize=None,
                                compression=None, nrows=None,
                                storage_options=None,
                                dtype_backend='pyarrow', engine='ujson')

                      .merge(right=read_json(
                                DOC_INFO_URL,
                                orient='records', typ='frame',
                                dtype=True, convert_axes=True,
                                convert_dates=True, keep_default_dates=True,
                                precise_float=False, date_unit=None,
                                encoding='utf-8', encoding_errors='strict',
                                lines=True, chunksize=None,
                                compression=None, nrows=None,
                                storage_options=None,
                                dtype_backend='pyarrow', engine='ujson'),

                             how='left', on='doc_name',  # left_on='doc_name', right_on='doc_name',
                             left_index=False, right_index=False,
                             sort=False,
                             suffixes=('', '_'),
                             copy=False,
                             indicator=False,
                             validate=None  # TODO: 'many_to_one' after Patronus AI fixes FOOTLOCKER_2022_annualreport
                             )

                      .set_index(keys=FB_ID_COL_NAME,
                                 drop=True, append=False,
                                 inplace=False,
                                 verify_integrity=True))

META_DF.fillna(value='', method=None, axis=None, inplace=True, limit=None)  # replace PyArrow NAs

LEGACY_META_DF: DataFrame = read_csv(METADATA_CSV_URL,
                                     sep=',',  # delimiter=',',
                                     header='infer', names=None, index_col=FB_ID_COL_NAME, usecols=None,
                                     dtype=None, engine='pyarrow', converters=None, true_values=None, false_values=None,
                                     skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None,
                                     na_values=None, na_filter=None, keep_default_na=True,
                                     skip_blank_lines=True,
                                     parse_dates=False, date_format=None, dayfirst=False, cache_dates=True,
                                     iterator=False, chunksize=None, compression=None,
                                     thousands=None, decimal='.',
                                     lineterminator=None,
                                     quotechar=None, quoting=0, doublequote=True,
                                     escapechar=None, comment=None,
                                     encoding='utf-8', encoding_errors='strict',
                                     dialect=None,
                                     on_bad_lines='error',
                                     low_memory=True, memory_map=False,
                                     float_precision=None,
                                     storage_options=None,
                                     dtype_backend='pyarrow')

assert (META_DF.index == LEGACY_META_DF.index).all()
# assert (META_DF.doc_name == LEGACY_META_DF.doc_name).all()  # J&J docs have been fixed
assert (META_DF.doc_period == LEGACY_META_DF.doc_period).all()
assert (META_DF.doc_link == LEGACY_META_DF.doc_link).all()
assert (META_DF.question_type == LEGACY_META_DF.question_type).all()
assert (META_DF.question == LEGACY_META_DF.question).all()
# assert (META_DF.answer == LEGACY_META_DF.answer).all()  # 01107 answer has been fixed

DOC_NAMES: list[DocName] = sorted(META_DF.doc_name.unique())
DOC_LINKS_BY_NAME: dict[DocName, str] = dict(zip(META_DF.doc_name, META_DF.doc_link))
DOC_NAMES_BY_FB_ID: dict[FbId, DocName] = META_DF.doc_name.to_dict()

FB_IDS: list[FbId] = META_DF.index.to_list()
FB_IDS_BY_DOC_NAME: dict[DocName, list[FbId]] = META_DF.groupby('doc_name').apply(lambda _: _.index.to_list())

QS_BY_FB_ID: dict[FbId, Question] = META_DF.question.to_dict()


DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'
DOCS_DATA_LOCAL_DIR_PATH: Path = DATA_LOCAL_DIR_PATH / 'docs'
OUTPUT_FILE_PATH: Path = DATA_LOCAL_DIR_PATH / 'output.csv'


GROUND_TRUTHS_FILE_PATH = Path(__file__).parent / 'ground-truths.yml'
with open(file=GROUND_TRUTHS_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    GROUND_TRUTHS: dict[FbId, GroundTruth] = yaml.safe_load(stream=f)

N_CASES: int = len(GROUND_TRUTHS)
CAT_DISTRIB: Counter[Category] = Counter(ground_truth['category'] for ground_truth in GROUND_TRUTHS.values())


EXPERTISE_DIR_PATH: Path = Path(__file__).parent / 'expertise'

EXPERT_KNOWLEDGE_FILE_PATH: Path = EXPERTISE_DIR_PATH / 'expert-knowledge.txt'
with open(file=EXPERT_KNOWLEDGE_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_KNOWLEDGE: str = f.read()

EXPERT_PROGRAMS_FILE_PATH: Path = EXPERTISE_DIR_PATH / 'expert-programs.yml'
with open(file=EXPERT_PROGRAMS_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_PROGRAMS: dict[ExpertPlanId, HTPDict] = yaml.safe_load(stream=f)

EXPERT_HTP_COMPANY_KEY: str = 'COMPANY'
EXPERT_HTP_PERIOD_KEY: str = 'PERIOD'


RAG_GROUND_TRUTHS_FILE_PATH: Path = Path(__file__).parent / 'rag-ground-truths.yml'
with open(file=RAG_GROUND_TRUTHS_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    RAG_GROUND_TRUTHS: RAGGroundTruths = yaml.safe_load(stream=f)


@dataclass
class Doc:
    name: DocName
    company: str = field(init=False, repr=False)
    period: str = field(init=False, repr=False)
    type: str = field(init=False, repr=False)

    def __post_init__(self):
        self.company, self.period, self.type = self.name.split(sep='_', maxsplit=2)

    def request(self) -> requests.Response:
        try:
            response: requests.Response = requests.get(
                url=(url := ((base64.b64decode(doc_link.split(sep=q, maxsplit=-1)[-1], altchars=None)
                              .decode(encoding='utf-8', errors='strict'))
                             if (q := '?pdfTarget=') in (doc_link := DOC_LINKS_BY_NAME[self.name])
                             else doc_link)),
                timeout=60,
                stream=True)

        except requests.exceptions.ConnectionError:
            response: requests.Response = requests.get(
                url=(url := f'{REPO_RAW_CONTENT_URL_PREFIX}/main/pdfs/{self.name}.pdf'),
                timeout=60,
                stream=True)

        if response.headers.get('Content-Type') != 'application/pdf':
            response: requests.Response = requests.get(url=url,
                                                       headers=NON_BOT_REQUEST_HEADERS,
                                                       timeout=60,
                                                       stream=True)

        return response

    @cached_property
    def dir_path(self) -> Path:
        dir_path: Path = DOCS_DATA_LOCAL_DIR_PATH / self.name

        if not (file_path := dir_path / f'{self.name}.pdf').is_file():
            dir_path.mkdir(parents=True, exist_ok=True)

            response: requests.Response = self.request()

            with open(file=file_path, mode='wb', buffering=-1, encoding=None, newline=None, closefd=True, opener=None) as f:
                f.write(response.content)

        return dir_path

    @cached_property
    def file_path(self) -> Path:
        return self.dir_path / f'{self.name}.pdf'


def create_or_update_ground_truths() -> dict[FbId, GroundTruth]:
    ground_truths: dict[FbId, GroundTruth] = {fb_id: {'sector': row.gics_sector,
                                                      'company': row.company, 'period': row.doc_period, 'doc-type': row.doc_type,
                                                      'doc': row.doc_name,
                                                      'question-type': row.question_type,
                                                      'question-reasoning': row.question_reasoning,
                                                      'domain-question-num': row.domain_question_num,
                                                      'question': row.question,
                                                      'answer': row.answer, 'justification': row.justification,
                                                      'page(s)-0based': row.evidence[0]['evidence_page_num']}
                                              for fb_id, row in META_DF.iterrows()}

    if GROUND_TRUTHS_FILE_PATH.is_file():
        with open(file=GROUND_TRUTHS_FILE_PATH,
                  buffering=-1,
                  encoding='utf-8',
                  errors='strict',
                  newline=None,
                  closefd=True,
                  opener=None) as f:
            existing_ground_truths: dict[FbId, GroundTruth] = yaml.safe_load(stream=f)

        for fb_id, ground_truth in ground_truths.items():
            if (existing_ground_truth := existing_ground_truths.get(fb_id)):
                for existing_key in set(existing_ground_truth).difference(ground_truth):
                    ground_truth[existing_key] = existing_ground_truth[existing_key]

    with open(file=GROUND_TRUTHS_FILE_PATH,
              mode='w',
              buffering=-1,
              encoding='utf-8',
              errors='strict',
              newline=None,
              closefd=True,
              opener=None) as f:
        yaml.safe_dump(data=ground_truths,
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

    return ground_truths


def get_or_create_output_df() -> DataFrame:
    output_df: DataFrame = (read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)
                            if OUTPUT_FILE_PATH.is_file()
                            else META_DF[['doc_name', 'question', 'answer']])

    output_df.loc[:, 'category'] = [GROUND_TRUTHS[fb_id]['category'] for fb_id in output_df.index]

    return output_df
