import argparse
from collections import Counter, defaultdict
from functools import cache
from pprint import pprint

from dotenv import load_dotenv
from loguru import logger
from pandas import DataFrame, read_csv
from tqdm import tqdm

from openssa.utils.llms import AnLLM, OpenAILLM

# pylint: disable=wrong-import-order
from data import (FbId, Question, Answer,
                  FB_ID_COL_NAME, GROUND_TRUTHS, OUTPUT_FILE_PATH)


EVAL_PROMPT_TEMPLATE: str = \
"""
I need you to act as an objective and precise judge of question-answering correctness.

Given the posed PROBLEM below, evaluate whether the ANSWER below is adequate and correct
according to the criteria described in the CORRECTNESS EVALUATION RUBRIC below.
The evaluation should regard the ANSWER as responding to the QUESTION,
and hence the ANSWER does not need to repeat contextual information already in the QUESTION.
Use no other information.

Output only a single word: YES if you judge the answer to be correct, and NO if incorrect.

QUESTION:
```
{question}
```

ANSWER TO EVALUATE:
```
{answer}
```

CORRECTNESS EVALUATION RUBRIC:
```
{rubric}
```
"""  # noqa: E122


load_dotenv()


@cache
def get_llm(model='gpt-4-1106-preview') -> AnLLM:
    return OpenAILLM(model=model, temperature=0.1)


def eval_correctness(fb_id: FbId, answer: Answer) -> str:
    question: Question = GROUND_TRUTHS[fb_id]['question']
    rubric: str = GROUND_TRUTHS[fb_id]['correctness']

    llm: AnLLM = get_llm()

    score: str = ''

    while score not in ('YES', 'NO'):
        score: str = llm.get_response(prompt=EVAL_PROMPT_TEMPLATE.format(question=question, answer=answer, rubric=rubric))  # noqa: E501

    if score == 'NO':
        logger.warning(f'QUESTION #{fb_id}:\n{question}\n'
                       '\n'
                       f'ANSWER JUDGED TO BE INADEQUATE/INCORRECT:\n{answer}\n'
                       '\n'
                       f'RUBRIC:\n{rubric}' +
                       ('\n\n(*** EXPERT ANSWER KNOWN TO BE INDEQUATE ***)'
                        if GROUND_TRUTHS[fb_id].get('answer-inadequate')
                        else ''))

    return score


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('answer_col', help='Name of the column containing answers to evaluate')
    arg_parser.add_argument('--id', default='all', help='FinanceBench Case ID')
    args = arg_parser.parse_args()

    output_df: DataFrame = read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)

    if 'all' in args.id.lower():
        n_yes_scores_by_category: defaultdict = defaultdict(int)

        for fb_id, answer in output_df[args.answer_col].items():
            n_yes_scores_by_category[GROUND_TRUTHS[fb_id]['category']] += \
                (eval_correctness(fb_id=fb_id, answer=answer) == 'YES')

        logger.info(f'TOTAL CORRECT: {(n := sum(n_yes_scores_by_category.values()))} / {(N := len(GROUND_TRUTHS))} = {n / N:.3f}')  # noqa: E501

        pprint({category: f'{(n := n_yes_scores_by_category[category])} / {n_for_category} = {n / n_for_category:.3f}'
                for category, n_for_category in Counter(_['category'] for _ in GROUND_TRUTHS.values()).items()})

    else:
        logger.info(eval_correctness(fb_id=args.id, answer=output_df.loc[args.id, args.answer_col]))
