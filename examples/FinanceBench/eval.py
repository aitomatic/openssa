import argparse

from collections import Counter
from dotenv import load_dotenv
from loguru import logger
import pandas as pd
from tqdm import tqdm

from openssa.utils.llms import OpenAILLM

# pylint: disable=wrong-import-order
from data import FB_ID_COL_NAME, GROUND_TRUTHS, OUTPUT_FILE_PATH


EVAL_PROMPT_TEMPLATE = \
"""
I need you to act as an objective and precise judge of the correctness of an answer to the QUESTION posed below.

Evaluate whether the ANSWER below is correct according to the grading criteria described in the EVALUATION RUBRIC.

Output only a single word. Say YES if you judge the answer to be correct, and NO if incorrect.

QUESTION:
```
{question}
```

ANSWER:
```
{answer}
```

EVALUATION RUBRIC:
```
{rubric}
```
"""  # noqa: E122


load_dotenv()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("answer_col", type=str, help="Name of the column containing answers")
    parser.add_argument("--id", type=str, help="FinanceBench Question ID", default="all")
    return parser.parse_args()


def get_eval_prompt(financebench_id, output_df, answer_col):
    return EVAL_PROMPT_TEMPLATE.format(question=GROUND_TRUTHS[financebench_id]['question'],
                                       answer=output_df.loc[financebench_id, answer_col],
                                       rubric=GROUND_TRUTHS[financebench_id]['correctness'])


def get_llm(model="gpt-4-1106-preview"):
    return OpenAILLM(model=model)


def evaluate_question(financebench_id, output_df, answer_col):
    prompt = get_eval_prompt(financebench_id, output_df, answer_col)
    llm = get_llm()
    return llm.get_response(prompt=prompt)


def main():
    args = parse_arguments()
    answer_col = args.answer_col
    financebench_id = args.id

    output_df = pd.read_csv(OUTPUT_FILE_PATH, index_col=FB_ID_COL_NAME)

    if financebench_id == "all":
        n_yes_scores_by_category = {}

        for fbid in tqdm(output_df.index):
            score = evaluate_question(fbid, output_df, answer_col)

            if score == 'YES':
                category = GROUND_TRUTHS[fbid]['category']
                if category in n_yes_scores_by_category:
                    n_yes_scores_by_category[category] += 1
                else:
                    n_yes_scores_by_category[category] = 1

            else:
                logger.warning(
                    f'QUESTION:\n{GROUND_TRUTHS[fbid]['question']}\n'
                    '\n'
                    f'ANSWER JUDGED TO BE WRONG:\n{output_df.loc[fbid, answer_col]}\n'
                    '\n'
                    f'RUBRIC:\n{GROUND_TRUTHS[fbid]['correctness']}')

        n_questions_by_category = Counter(_['category'] for _ in GROUND_TRUTHS.values())
        yes_proportions_by_category = {c: n_yes_scores_by_category[c] / n_questions_by_category[c]
                                       for c in n_questions_by_category}
        logger.info(yes_proportions_by_category)

    else:
        score = evaluate_question(financebench_id, output_df, answer_col)
        print(score)


if __name__ == "__main__":
    main()
