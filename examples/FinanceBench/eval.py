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
from data import FbId, Question, Answer, FB_ID_COL_NAME, GROUND_TRUTHS, OUTPUT_FILE_PATH


EVAL_PROMPT_TEMPLATE: str = \
"""You shall act as a judge of question-answering adequacy and correctness.

Given the posed QUESTION below, evaluate whether the ANSWER below is adequate and correct
according to the criteria described in the CORRECTNESS EVALUATION RUBRIC below.
The evaluation should regard the ANSWER as responding to the QUESTION,
and hence the ANSWER does not need to repeat contextual information already in the QUESTION.

Financial and technical terminology can be treated as case-insensitive.

Use no other information.

Output only a single word, either:
- YES: if you judge the ANSWER to be adequate and correct; or
- NO: if you judge the ANSWER to be inadequate or incorrect.

QUESTION:
---------
```
{question}
```

ANSWER TO EVALUATE:
-------------------
```
{answer}
```

CORRECTNESS EVALUATION RUBRIC:
------------------------------
```
{rubric}
```
"""  # noqa: E122


load_dotenv()


@cache
def get_llm(model='gpt-4-1106-preview') -> AnLLM:
    return OpenAILLM(model=model, temperature=0)


def eval_correctness(fb_id: FbId, answer: Answer, n_times: int = 9, debug: bool = False) -> str:
    question: Question = GROUND_TRUTHS[fb_id]['question']
    rubric: str = GROUND_TRUTHS[fb_id]['correctness']
    prompt: str = EVAL_PROMPT_TEMPLATE.format(question=question, answer=answer, rubric=rubric)

    llm: AnLLM = get_llm()

    for _ in range(n_times):
        score: str = ''

        while score not in ('YES', 'NO'):
            score: str = llm.get_response(prompt=prompt)

        if score == 'NO':
            break

    if score == 'NO':
        logger.warning(f'QUESTION #{fb_id}:\n{question}\n'
                       '\n'
                       f'ANSWER JUDGED TO BE INADEQUATE/INCORRECT:\n{answer}\n'
                       '\n'
                       f'RUBRIC:\n{rubric}' +
                       ('\n\n(*** EXPERT ANSWER KNOWN TO BE INDEQUATE ***)'
                        if GROUND_TRUTHS[fb_id].get('answer-inadequate')
                        else ''))
        if debug:
            logger.debug(f'PROMPT:\n{prompt}')

    return score


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('answer_col', help='Name of the column containing answers to evaluate')
    arg_parser.add_argument('--id', default='all', help='FinanceBench Case ID')
    arg_parser.add_argument('--n-times', type=int, default=9, help='Number of times to evaluate')
    arg_parser.add_argument('--debug', action='store_true', help='Debug by printing out prompts')
    args = arg_parser.parse_args()

    output_df: DataFrame = read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)

    if 'all' in args.id.lower():
        n_yes_scores_by_category: defaultdict = defaultdict(int)

        for fb_id, answer in tqdm(output_df[args.answer_col].items(), total=(N := len(GROUND_TRUTHS))):
            n_yes_scores_by_category[GROUND_TRUTHS[fb_id]['category']] += \
                (eval_correctness(fb_id=fb_id, answer=answer, n_times=args.n_times, debug=args.debug) == 'YES')

        logger.info(f'TOTAL CORRECT: {(n := sum(n_yes_scores_by_category.values()))} / {N} = {n / N:.3f}')

        pprint({category: f'{(n := n_yes_scores_by_category[category])} / {n_for_category} = {n / n_for_category:.3f}'
                for category, n_for_category in Counter(_['category'] for _ in GROUND_TRUTHS.values()).items()})

    else:
        logger.info(eval_correctness(fb_id=args.id, answer=output_df.loc[args.id, args.answer_col],
                                     n_times=args.n_times, debug=args.debug))
