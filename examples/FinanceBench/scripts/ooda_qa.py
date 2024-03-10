import os
from loguru import logger
import nest_asyncio
import pandas as pd
from openssa.utils.utils import Utils
from openssa.core.ooda_rag.solver import OodaSSA

nest_asyncio.apply()

PATH: str = "./tmp/finance-bench/docs"
FINANCEBENCH_CSV: str = "./tmp/finance-bench/finance_bench_dataset.csv"
OUTPUT_DIRECTORY: str = "tmp/finance-bench/output"
OUTPUT_FILE_NAME: str = "ooda_rag_output.csv"


@Utils.timeit
def process_doc(doc_name: str, question: str) -> str:
    ssa = OodaSSA(enable_generative=True)
    resource = os.path.join(PATH, doc_name)
    ssa.activate_resources(resource)
    solution = ssa.solve(question)
    return solution


def run():
    output_file_path = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILE_NAME)
    answer_column_name = "ooda_answer"
    # Check if the output file exists, and read from it if available (load cache)
    if os.path.exists(output_file_path):
        df_finbench = pd.read_csv(output_file_path)
    else:
        # If the output file does not exist, read from the original dataset
        df_finbench = pd.read_csv(FINANCEBENCH_CSV)
        if answer_column_name not in df_finbench.columns:
            df_finbench[answer_column_name] = ""
    df_finbench = df_finbench.fillna("")

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    for index, row in df_finbench.iterrows():
        logger.info(f"Processing row {index} of {len(df_finbench)} : {row['doc_name']}")
        if row["status"] == "ok" and not row[answer_column_name]:
            doc_name = row["doc_name"]
            question = row["question"]
            answer = process_doc(doc_name, question)
            df_finbench.loc[index, answer_column_name] = answer
            # Save progress as cache after processing each row
            df_finbench.to_csv(output_file_path, index=False)
        print(f"complete index {index} of {len(df_finbench)}")

    # if any answer contain "Empty Response" then update it to "file error"
    df_finbench.loc[
        df_finbench[answer_column_name].str.lower().str.contains("empty response"),
        answer_column_name,
    ] = "file reading error"

    df_finbench.to_csv(output_file_path, index=False)
    print("Processing complete. Output saved to:", output_file_path)


def clean_up():
    file_path = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILE_NAME)
    df_data = pd.read_csv(file_path)
    filtered_df = df_data[
        ~df_data["ooda_answer"].isna()
        & (df_data["ooda_answer"] != "file reading error")
    ]
    clean_output_file_path = os.path.join(
        OUTPUT_DIRECTORY, "filtered_ooda_rag_output.csv"
    )
    filtered_df.to_csv(clean_output_file_path, index=False)
    print(f"Filtered data saved to {clean_output_file_path}")


if __name__ == "__main__":
    run()
