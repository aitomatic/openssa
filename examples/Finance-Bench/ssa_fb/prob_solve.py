# pylint: disable=bare-except,no-name-in-module,wrong-import-position


from argparse import ArgumentParser
from pathlib import Path
import sys

import nest_asyncio
from pandas import DataFrame, read_csv
from tqdm import tqdm

sys.path.append(str(Path(__file__).parent.parent))

from ssa_fb.data import META_DF, OUTPUT_FILE_PATH  # noqa: E402
from ssa_fb.ssas import get_or_create_ooda_ssa  # noqa: E402


def solve(financebench_id: str) -> str:
    if financebench_id.lower().strip() == 'all':
        nest_asyncio.apply()

        for _financebench_id in tqdm(META_DF.financebench_id):
            print(solve(_financebench_id))

        return None

    matching_fbid_row_num: int = (META_DF.financebench_id == financebench_id).idxmax()

    problem: str = META_DF.at[matching_fbid_row_num, 'question']
    print(f'PROBLEM: "{problem}"')

    doc_name: str = META_DF.at[matching_fbid_row_num, 'doc_name']
    ssa = get_or_create_ooda_ssa(doc_name)

    print('SOLVING...')
    try:
        solution = ssa.solve(problem)
    except:  # noqa: E722
        return None

    if OUTPUT_FILE_PATH.is_file():
        output_df: DataFrame = read_csv(OUTPUT_FILE_PATH)

    else:
        output_df: DataFrame = META_DF[['financebench_id', 'doc_name',
                                        'question', 'evidence_text', 'page_number', 'answer']]
        output_df['OodaSSA-answer'] = ''

    output_df.loc[matching_fbid_row_num, 'OodaSSA-answer'] = solution
    output_df.to_csv(OUTPUT_FILE_PATH, index=False)

    return solution


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('financebench_id')

    args = arg_parser.parse_args()

    print(solve(args.financebench_id))
