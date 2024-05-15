from __future__ import annotations

from argparse import ArgumentParser
from typing import TYPE_CHECKING

from loguru import logger

from data_and_knowledge import DocName, Doc, RAG_GROUND_TRUTHS
from eval import get_lm, EVAL_PROMPT_TEMPLATE
from rag_default import get_or_create_file_resource

if TYPE_CHECKING:
    from openssa.l2.resource.file import FileResource
    from openssa.l2.util.lm.abstract import AnLM


DEFS: dict[str, str] = RAG_GROUND_TRUTHS['defs']


QUESTION_PROMPT_TEMPLATE: str = ('what is value in dollars of {line_item} on {statement} of {company} '
                                 'as at / for {fiscal_period} fiscal period?')

EVAL_RUBRIC_TEMPLATE: str = 'the answer contains a quantity equivalent to or approximately equal to {ground_truth}'

EVAL_LM: AnLM = get_lm()


def test_rag(doc_name: DocName, n_repeats_per_eval: int = 9):  # pylint: disable=too-many-locals
    doc: Doc = Doc(name=doc_name)
    file_resource: FileResource = get_or_create_file_resource(doc_name=doc_name)

    for statement_id, line_item_details in RAG_GROUND_TRUTHS['ground-truths'][doc_name].items():
        statement: str = DEFS[statement_id]

        for line_item_id, fiscal_periods_and_ground_truths in line_item_details.items():
            line_item: str = DEFS[line_item_id]

            for fiscal_period, ground_truth in fiscal_periods_and_ground_truths.items():
                eval_prompt: str = EVAL_PROMPT_TEMPLATE.format(
                    question=(question := QUESTION_PROMPT_TEMPLATE.format(line_item=line_item,
                                                                          statement=statement,
                                                                          company=doc.company,
                                                                          fiscal_period=fiscal_period)),
                    answer=(answer := file_resource.answer(question=question)),
                    rubric=(rubric := EVAL_RUBRIC_TEMPLATE.format(ground_truth=ground_truth)))

                for _ in range(n_repeats_per_eval):
                    score: str = ''

                    while score not in {'YES', 'NO'}:
                        score: str = EVAL_LM.get_response(prompt=eval_prompt, temperature=0)

                    if score == 'NO':
                        logger.warning(f'QUESTION re: {doc_name}:\n{question}\n'
                                       '\n'
                                       f'ANSWER JUDGED TO BE INCORRECT:\n{answer}\n'
                                       '\n'
                                       f'RUBRIC:\n{rubric}')


arg_parser = ArgumentParser()
arg_parser.add_argument('doc_name')
args = arg_parser.parse_args()

test_rag(doc_name=args.doc_name)
