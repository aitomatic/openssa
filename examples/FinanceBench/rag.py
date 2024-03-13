import os
from loguru import logger
import nest_asyncio
import pandas as pd
from openssa.core.ooda_rag.custom import CustomSSM
from openssa.utils.utils import Utils

from data import OUTPUT_FILE_PATH

nest_asyncio.apply()

PATH = "./tmp/finance-bench/docs"
FINANCEBENCH_CSV: str = "./tmp/finance-bench/finance_bench_dataset.csv"
OUTPUT_DIRECTORY = "tmp/finance-bench/output"


@Utils.timeit
def process_doc(doc_name: str, question: str) -> str:
    ssm = CustomSSM()
    ssm.read_directory(os.path.join(PATH, doc_name))
    ooda_answer = ssm.discuss(question).get("content")
    return ooda_answer


def run():
    output_file_path = os.path.join(OUTPUT_DIRECTORY, "standard_rag_output.csv")
    answer_column_name = "rag_answer"
    # Check if the output file exists, and read from it if available
    if os.path.exists(output_file_path):
        df_finbench = pd.read_csv(output_file_path)
    else:
        # If the output file does not exist, read from the original dataset
        df_finbench = pd.read_csv(FINANCEBENCH_CSV)
        if answer_column_name not in df_finbench.columns:
            df_finbench[answer_column_name] = ""

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    for index, row in df_finbench.iterrows():
        logger.info(f"Processing row {index} of {len(df_finbench)} : {row['doc_name']}")
        if row["status"] == "ok" and not row[answer_column_name]:
            doc_name = row["doc_name"]
            question = row["question"]
            answer = process_doc(doc_name, question)
            df_finbench.loc[index, answer_column_name] = answer
            # Save progress after processing each row
            df_finbench.to_csv(output_file_path, index=False)

    print("Processing complete. Output saved to:", output_file_path)


if __name__ == "__main__":
    run()
