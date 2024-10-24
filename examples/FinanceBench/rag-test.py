from argparse import ArgumentParser

from loguru import logger

from openssa import LMConfig

# pylint: disable=wrong-import-order
from data_and_knowledge import DocName, Doc, RAG_GROUND_TRUTHS
from eval import get_lm, EVAL_PROMPT_TEMPLATE
from rag import get_or_create_file_resource


DEFS: dict[str, str] = RAG_GROUND_TRUTHS['defs']


QUESTION_PROMPT_TEMPLATE: str = (
    'What is value in dollars of `{line_item}` (or most similar-meaning reported line item) '
    'on `{statement}` (or most similar-meaning statement) of {company} '
    '(and NOT such statement(s) of its business segments/units, or of its acquired and/or divested companies) '
    'as at / for {fiscal_period} fiscal period?'
)

EVAL_RUBRIC_TEMPLATE: str = 'the answer contains a quantity equivalent to or approximately equal to {ground_truth}'

EVAL_LM = get_lm()


def test_rag(doc_name: DocName, n_repeats_per_eval: int = 9,
             llama_index_openai_lm_name: str = LMConfig.OPENAI_DEFAULT_SMALL_MODEL):
    # pylint: disable=too-many-locals
    doc: Doc = Doc(name=doc_name)
    file_resource = get_or_create_file_resource(doc_name=doc_name, llama_index_openai_lm_name=llama_index_openai_lm_name)  # noqa: E501

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
                    rubric=EVAL_RUBRIC_TEMPLATE.format(ground_truth=ground_truth))

                for _ in range(n_repeats_per_eval):
                    score: str = ''

                    while score not in {'YES', 'NO'}:
                        score: str = EVAL_LM.get_response(prompt=eval_prompt, temperature=0)

                    if score == 'NO':
                        logger.warning(f'\n{doc_name}:\n{question}\n'
                                       '\n'
                                       f'ANSWER JUDGED TO BE INCORRECT:\n{answer}\n'
                                       '\n'
                                       f'GROUND TRUTH:\n{ground_truth}\n')
                        break

                else:
                    logger.info(f'\n{doc_name}:\n{question}\n'
                                '\n'
                                f'ANSWER JUDGED TO BE CORRECT:\n{answer}\n'
                                '\n'
                                f'GROUND TRUTH:\n{ground_truth}\n')


arg_parser = ArgumentParser()
arg_parser.add_argument('doc_name')
arg_parser.add_argument('--gpt4o', action='store_true', default=False)
args = arg_parser.parse_args()

test_rag(doc_name=args.doc_name, llama_index_openai_lm_name=(LMConfig.OPENAI_DEFAULT_MODEL
                                                             if args.gpt4o
                                                             else LMConfig.OPENAI_DEFAULT_SMALL_MODEL))
