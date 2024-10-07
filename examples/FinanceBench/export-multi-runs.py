from argparse import ArgumentParser

from pandas import DataFrame, read_csv

from data_and_knowledge import FB_ID_COL_NAME, DATA_LOCAL_DIR_PATH


EXPORT_FILE_NAME: str = 'export-multi-runs.csv'


arg_parser = ArgumentParser()
arg_parser.add_argument('output_name')
arg_parser.add_argument('output_file_names', nargs='+')
args = arg_parser.parse_args()


for i, df in enumerate(read_csv(DATA_LOCAL_DIR_PATH / output_file_name, index_col=FB_ID_COL_NAME)
                       for output_file_name in args.output_file_names):
    if not i:
        export_df: DataFrame = df[['question']]

    export_df.loc[:, f'answer {i + 1}'] = df[args.output_name]  # pylint: disable=possibly-used-before-assignment


export_df.to_csv(DATA_LOCAL_DIR_PATH / EXPORT_FILE_NAME, index=True)
