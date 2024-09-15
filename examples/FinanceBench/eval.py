from __future__ import annotations

import argparse
from collections import defaultdict
from functools import cache
from pprint import pprint
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from loguru import logger
from pandas import DataFrame, notna, read_csv
from tqdm import tqdm

from openssa.core.util.lm.config import LMConfig
from openssa.core.util.lm.openai import OpenAILM

# pylint: disable=wrong-import-order
from data_and_knowledge import (FbId, Question, Answer, Category, GroundTruth,
                                FB_ID_COL_NAME, GROUND_TRUTHS, N_CASES, CAT_DISTRIB,
                                LOCAL_CACHE_DIR_PATH, OUTPUT_FILE_PATH, get_or_create_output_df)
from log import switch_log_file

if TYPE_CHECKING:
    from openssa.core.util.lm.abstract import AbstractLM


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
def get_lm(model='gpt-4o') -> AbstractLM:
    return OpenAILM(model=model, api_key=LMConfig.OPENAI_API_KEY, api_base=LMConfig.OPENAI_API_URL)


def human_eval_recommended(fb_id: FbId) -> bool | None:
    return (ground_truth := GROUND_TRUTHS[fb_id]).get('answer-inadequate') or ground_truth.get('evaluator-unreliable')


def eval_correctness(fb_id: FbId, answer: Answer, output_name: str | None = None,  # pylint: disable=too-many-arguments
                     n_times: int = 9, human: bool = True, debug: bool = False) -> bool:
    if output_name:
        switch_log_file(fb_id=fb_id, output_name=output_name)

    question: Question = (ground_truth := GROUND_TRUTHS[fb_id])['question']
    rubric: str = ground_truth['correctness']
    prompt: str = EVAL_PROMPT_TEMPLATE.format(question=question, answer=answer, rubric=rubric)

    lm: AbstractLM = get_lm()

    for _ in range(n_times):
        score: str = ''

        while score not in {'YES', 'NO'}:
            score: str = lm.get_response(prompt=prompt, temperature=0)

        if score == 'NO':
            logger.warning(f'\n{fb_id}\n{ground_truth['doc']}:\n{question}\n'
                           '\n'
                           f'ANSWER JUDGED TO BE INCORRECT:\n{answer}\n'
                           '\n'
                           f'RUBRIC:\n{rubric}' +
                           ('\n\n(*** EXPERT ANSWER KNOWN TO BE INADEQUATE ***)\n'
                            if GROUND_TRUTHS[fb_id].get('answer-inadequate')
                            else '\n'))

            if debug:
                logger.debug(f'PROMPT:\n{prompt}')

            if human and human_eval_recommended(fb_id=fb_id):
                human_eval_str: str = ''
                while not human_eval_str:
                    human_eval_str: str = input('\n*** HUMAN EVALUATION ***: if answer is correct, type "Y": ').strip()

                correct: bool = human_eval_str.lower().startswith('y')

            else:
                correct: bool = False

            break

    else:
        correct: bool = True

    if output_name:
        output_df: DataFrame = get_or_create_output_df()
        output_df.loc[fb_id, f'{output_name}---CORRECTNESS']: bool = correct
        output_df.to_csv(OUTPUT_FILE_PATH, index=True)

    return correct


def eval_all(output_name: str, refresh: bool = True, n_times: int = 9, human: bool = True, debug: bool = False):
    # pylint: disable=too-many-locals
    output_df: DataFrame = get_or_create_output_df()

    n_yes_scores_by_category: defaultdict = defaultdict(int)
    incorrect_answer_fb_ids: dict[FbId, str] = {}

    for fb_id, answer in tqdm(output_df[output_name].items(), total=N_CASES):
        ground_truth: GroundTruth = GROUND_TRUTHS[fb_id]

        if (eval_correctness(fb_id=fb_id, answer=answer, output_name=output_name, n_times=n_times, human=human, debug=debug)  # noqa: E501
                if refresh
                else (notna(correctness := output_df.loc[fb_id, f'{output_name}---CORRECTNESS']) and correctness)):
            n_yes_scores_by_category[ground_truth['category']] += 1

        else:
            incorrect_answer_fb_ids[fb_id]: str = ('expert answer inadequate'
                                                   if ground_truth.get('answer-inadequate')
                                                   else ('evaluator unreliable'
                                                         if ground_truth.get('evaluator-unreliable')
                                                         else ''))

    logger.info(f'TOTAL CORRECT: {(n := sum(n_yes_scores_by_category.values()))} / {N_CASES} = {n / N_CASES:.1%}')

    pprint(correctness_by_category := {category: (f'{(n := n_yes_scores_by_category[category])} / {n_for_category} '
                                                  f'= {n / n_for_category:.1%}')
                                       for category, n_for_category in CAT_DISTRIB.items()})

    pprint({
        'EASY': (f'{(e := sum(n_yes_scores_by_category[easy_cat]
                              for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} / '
                 f'{(se := sum(CAT_DISTRIB[easy_cat]
                               for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} '
                 f'= {e / se:.1%}'),

        'HARD': (f'{(h := sum(n_yes_scores_by_category[hard_cat]
                              for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                               Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} / '
                 f'{(sh := sum(CAT_DISTRIB[hard_cat]
                               for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                                Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} '
                 f'= {h / sh:.1%}')
    })

    logger.warning('INCORRECT:')
    pprint(incorrect_answer_fb_ids)

    return correctness_by_category


def compare_eval(output_name: str, baseline_output_name: str = 'RAG-Default'):
    output_df: DataFrame = get_or_create_output_df()

    baseline_correctness_by_category: dict[str, str] = eval_all(output_name=baseline_output_name, refresh=False)
    correctness_by_category: dict[str, str] = eval_all(output_name=output_name, refresh=False)
    pprint({category: {output_name: correctness_summary, baseline_output_name: baseline_correctness_by_category[category]}
            for category, correctness_summary in correctness_by_category.items()})

    output_df.loc[:, baseline_output_name] = output_df[f'{baseline_output_name}---CORRECTNESS']
    output_df.loc[:, output_name] = output_df[f'{output_name}---CORRECTNESS']
    return output_df.loc[output_df[output_name] != output_df[baseline_output_name],
                         ['doc_name', 'category', baseline_output_name, output_name]]


def eval_accuracy_and_consistency_wrt_ground_truths(output_name: str, output_file_names: list[str]):
    # pylint: disable=too-many-locals

    n_output_files: int = len(output_file_names)
    correctness_col_name: str = f'{output_name}---CORRECTNESS'

    n_yes_scores_by_fb_id: defaultdict = defaultdict(int)
    incorrect_answer_fb_ids: dict[FbId, str] = {}

    for output_df in (read_csv(LOCAL_CACHE_DIR_PATH / output_file_name, index_col=FB_ID_COL_NAME)
                      for output_file_name in output_file_names):

        for fb_id, correctness in output_df[correctness_col_name].items():
            ground_truth: GroundTruth = GROUND_TRUTHS[fb_id]

            if notna(correctness) and correctness:
                n_yes_scores_by_fb_id[fb_id] += 1

            else:
                incorrect_answer_fb_ids[fb_id]: str = ('expert answer inadequate'
                                                       if ground_truth.get('answer-inadequate')
                                                       else ('evaluator unreliable'
                                                             if ground_truth.get('evaluator-unreliable')
                                                             else ''))

    cumu_avg_accuracy_scores_by_category: defaultdict = defaultdict(int)
    cumu_consistency_scores_by_category: defaultdict = defaultdict(float)

    for fb_id, ground_truth in GROUND_TRUTHS.items():
        cumu_avg_accuracy_scores_by_category[cat := ground_truth['category']] += (a := n_yes_scores_by_fb_id[fb_id] / n_output_files)
        cumu_consistency_scores_by_category[cat] += 2 * abs(a - 0.5)

    print(f'TOTAL CORRECT: {(n := sum(cumu_avg_accuracy_scores_by_category.values()))} / {N_CASES} = {n / N_CASES:.1%}')

    pprint({category: (f'{(n := cumu_avg_accuracy_scores_by_category[category])} / {n_for_category} '
                       f'= {n / n_for_category:.1%}')
            for category, n_for_category in CAT_DISTRIB.items()})

    pprint({
        'EASY': (f'{(e := sum(cumu_avg_accuracy_scores_by_category[easy_cat]
                              for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} / '
                 f'{(se := sum(CAT_DISTRIB[easy_cat]
                               for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} '
                 f'= {e / se:.1%}'),

        'HARD': (f'{(h := sum(cumu_avg_accuracy_scores_by_category[hard_cat]
                              for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                               Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} / '
                 f'{(sh := sum(CAT_DISTRIB[hard_cat]
                               for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                                Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} '
                 f'= {h / sh:.1%}')
    })

    print(f'\nTOTAL CONSISTENT: {(n := sum(cumu_consistency_scores_by_category.values()))} / {N_CASES} = {n / N_CASES:.1%}')

    pprint({category: (f'{(n := cumu_consistency_scores_by_category[category])} / {n_for_category} '
                       f'= {n / n_for_category:.1%}')
            for category, n_for_category in CAT_DISTRIB.items()})

    pprint({
        'EASY': (f'{(e := sum(cumu_consistency_scores_by_category[easy_cat]
                              for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} / '
                 f'{(se := sum(CAT_DISTRIB[easy_cat]
                               for easy_cat in (Category.RETRIEVE, Category.COMPARE, Category.CALC_CHANGE)))} '
                 f'= {e / se:.1%}'),

        'HARD': (f'{(h := sum(cumu_consistency_scores_by_category[hard_cat]
                              for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                               Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} / '
                 f'{(sh := sum(CAT_DISTRIB[hard_cat]
                               for hard_cat in (Category.CALC_COMPLEX, Category.CALC_AND_JUDGE,
                                                Category.EXPLAIN_FACTORS, Category.OTHER_ADVANCED)))} '
                 f'= {h / sh:.1%}')
    })

    print('\nINCORRECT:')
    pprint(incorrect_answer_fb_ids)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('answer_col', help='Name of the column containing answers to evaluate')
    arg_parser.add_argument('--id', default='all', help='FinanceBench Case ID')
    arg_parser.add_argument('--n-times', type=int, default=9, help='Number of times to evaluate')

    arg_parser.add_argument('--human-eval', dest='human_eval', action='store_true', help='Human Evaluation ON')
    arg_parser.add_argument('--no-human-eval', dest='human_eval', action='store_false', help='Human Evaluation OFF')
    arg_parser.set_defaults(human_eval=True)

    arg_parser.add_argument('--refresh', dest='refresh', action='store_true', help='Evaluation Refreshing ON')
    arg_parser.add_argument('--no-refresh', dest='refresh', action='store_false', help='Evaluation Refreshing OFF')
    arg_parser.set_defaults(refresh=True)

    arg_parser.add_argument('--debug', action='store_true', help='Debug by printing out prompts')

    args = arg_parser.parse_args()

    if 'all' in args.id.lower():
        eval_all(output_name=args.answer_col, refresh=args.refresh, n_times=args.n_times, human=args.human_eval, debug=args.debug)  # noqa: E501

    else:
        logger.info(
            eval_correctness(fb_id=args.id,
                             answer=read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME).loc[args.id, args.answer_col],
                             output_name=args.answer_col,
                             n_times=args.n_times, human=args.human_eval, debug=args.debug))
