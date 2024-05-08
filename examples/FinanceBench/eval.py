import argparse
from collections import defaultdict
from functools import cache
from pprint import pprint

from dotenv import load_dotenv
from loguru import logger
from pandas import DataFrame, read_csv
from tqdm import tqdm

from openssa.l2.config import Config
from openssa.l2.util.lm.abstract import AnLM
from openssa.l2.util.lm.openai import OpenAILM

# pylint: disable=wrong-import-order
from data import FbId, Question, Answer, GroundTruth, FB_ID_COL_NAME, GROUND_TRUTHS, N_CASES, CAT_DISTRIB, OUTPUT_FILE_PATH  # noqa: E501


EVAL_PROMPT_TEMPLATE: str = \
"""You shall act as a judge of question-answering correctness.

Given the posed QUESTION below, evaluate whether the ANSWER below is correct
according to the criteria specified in the CORRECTNESS EVALUATION RUBRIC below.

- The evaluation should regard the ANSWER as responding to the QUESTION,
  and hence the ANSWER does not need to repeat contextual information already in the QUESTION;

- The evaluation should follow the RUBRIC strictly,
  not looking for in the ANSWER more elaboration/explanation than what the RUBRIC explicitly requires;

- Financial and technical terminology can be treated as case-insensitive.

Output only a single word, either:
- YES: if you judge the ANSWER to be correct; or
- NO: if you judge the ANSWER to be incorrect.

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
def get_lm(model='gpt-4-1106-preview') -> AnLM:
    return OpenAILM(model=model, api_key=Config.OPENAI_API_KEY, api_base=Config.OPENAI_API_URL)


def human_eval_recommended(fb_id: FbId) -> bool | None:
    return (ground_truth := GROUND_TRUTHS[fb_id]).get('answer-inadequate') or ground_truth.get('evaluator-unreliable')


def eval_correctness(fb_id: FbId, answer: Answer, n_times: int = 9, human: bool = True, debug: bool = False) -> bool:
    question: Question = GROUND_TRUTHS[fb_id]['question']
    rubric: str = GROUND_TRUTHS[fb_id]['correctness']
    prompt: str = EVAL_PROMPT_TEMPLATE.format(question=question, answer=answer, rubric=rubric)

    lm: AnLM = get_lm()

    for _ in range(n_times):
        score: str = ''

        while score not in {'YES', 'NO'}:
            score: str = lm.get_response(prompt=prompt, temperature=0)

        if score == 'NO':
            logger.warning(f'QUESTION #{fb_id}:\n{question}\n'
                           '\n'
                           f'ANSWER JUDGED TO BE INCORRECT:\n{answer}\n'
                           '\n'
                           f'RUBRIC:\n{rubric}' +
                           ('\n\n(*** EXPERT ANSWER KNOWN TO BE INADEQUATE ***)'
                            if GROUND_TRUTHS[fb_id].get('answer-inadequate')
                            else ''))

            if debug:
                logger.debug(f'PROMPT:\n{prompt}')

            if human and human_eval_recommended(fb_id=fb_id):
                human_eval_str: str = ''
                while not human_eval_str:
                    human_eval_str: str = input('\n*** HUMAN EVALUATION ***: if answer is correct, type "Y": ').strip()

                return human_eval_str.lower().startswith('y')

            return False

    return True


def eval_all(output_name: str, n_times: int = 9, human: bool = True, debug: bool = False):
    output_df: DataFrame = read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)

    n_yes_scores_by_category: defaultdict = defaultdict(int)
    incorrect_answer_fb_ids: dict[FbId, str] = {}

    for fb_id, answer in tqdm(output_df[output_name].items(), total=N_CASES):
        ground_truth: GroundTruth = GROUND_TRUTHS[fb_id]

        if eval_correctness(fb_id=fb_id, answer=answer, n_times=n_times, human=human, debug=debug):
            n_yes_scores_by_category[ground_truth['category']] += 1

        else:
            incorrect_answer_fb_ids[fb_id]: str = ('expert answer inadequate'
                                                   if ground_truth.get('answer-inadequate')
                                                   else ('evaluator unreliable'
                                                         if ground_truth.get('evaluator-unreliable')
                                                         else ''))

    logger.info(f'TOTAL CORRECT: {(n := sum(n_yes_scores_by_category.values()))} / {N_CASES} = {n / N_CASES:.1%}')
    pprint({category: f'{(n := n_yes_scores_by_category[category])} / {n_for_category} = {n / n_for_category:.1%}'
            for category, n_for_category in CAT_DISTRIB.items()})

    logger.warning('INCORRECT:')
    pprint(incorrect_answer_fb_ids)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('answer_col', help='Name of the column containing answers to evaluate')
    arg_parser.add_argument('--id', default='all', help='FinanceBench Case ID')
    arg_parser.add_argument('--n-times', type=int, default=9, help='Number of times to evaluate')

    arg_parser.add_argument('--human-eval', dest='human_eval', action='store_true', help='Human Evaluation ON')
    arg_parser.add_argument('--no-human-eval', dest='human_eval', action='store_false', help='Human Evaluation OFF')
    arg_parser.set_defaults(human_eval=True)

    arg_parser.add_argument('--debug', action='store_true', help='Debug by printing out prompts')

    args = arg_parser.parse_args()

    if 'all' in args.id.lower():
        eval_all(output_name=args.answer_col, n_times=args.n_times, human=args.human_eval, debug=args.debug)

    else:
        logger.info(
            eval_correctness(fb_id=args.id,
                             answer=read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME).loc[args.id, args.answer_col],
                             n_times=args.n_times, human=args.human_eval, debug=args.debug))
