from argparse import ArgumentParser

from data_and_knowledge import DocName, Answer, Doc, RAG_GROUND_TRUTHS
from rag_default import get_or_create_file_resource


DEFS: dict[str, str] = RAG_GROUND_TRUTHS['defs']


QUESTION_PROMPT_TEMPLATE: str = ('What is value in dollars of {line_item} on {statement} of {company} '
                                 'as at / for {fiscal_period} fiscal period?')


def test_rag(doc_name: DocName):
    doc: Doc = Doc(name=doc_name)

    for statement_id, line_item_details in RAG_GROUND_TRUTHS['ground-truths'][doc_name].items():
        statement: str = DEFS[statement_id]

        for line_item_id, fiscal_periods_and_ground_truths in line_item_details.items():
            line_item: str = DEFS[line_item_id]

            for fiscal_period, ground_truth in fiscal_periods_and_ground_truths.items():
                answer: Answer = (get_or_create_file_resource(doc_name=doc_name)
                                  .answer(question=QUESTION_PROMPT_TEMPLATE.format(line_item=line_item,
                                                                                   statement=statement,
                                                                                   company=doc.company,
                                                                                   fiscal_period=fiscal_period)))

                print(f'"{answer}" vs. "{ground_truth}"')


arg_parser = ArgumentParser()
arg_parser.add_argument('doc_name')
args = arg_parser.parse_args()

test_rag(doc_name=args.doc_name)
