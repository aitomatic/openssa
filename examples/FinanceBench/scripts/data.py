import os
from pathlib import Path
import pandas as pd
import requests
from requests.exceptions import HTTPError

# Note JOHNSON&JOHNSON is not downloadable

METADATA_URL: str = (
    "https://raw.githubusercontent.com/patronus-ai/"
    "financebench/main/financebench_sample_150.csv"
)


def download_dataset():
    # Read the CSV file
    df_finbench = pd.read_csv(METADATA_URL)
    df_finbench["status"] = "ok"

    base_directory = "tmp/finance-bench/docs"
    count = 0
    for index, row in df_finbench.iterrows():
        doc_name = row["doc_name"]
        doc_link = row["doc_link"]

        # Create a subdirectory for each document
        doc_directory = os.path.join(base_directory, doc_name)
        if not os.path.exists(doc_directory):
            os.makedirs(doc_directory)

        # Path for the PDF file
        file_path = os.path.join(doc_directory, f"{doc_name}.pdf")

        # Check if the file has already been downloaded
        if not Path(file_path).is_file():
            try:
                # Download the file
                response = requests.get(doc_link, timeout=30)
                response.raise_for_status()  # Raises if the HTTP request, returned an unsuccessful status code

                # Write the content to a file
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded and saved: {file_path}")
                count += 1
            except HTTPError as e:
                df_finbench.loc[index, "status"] = "error"  # Update the status to 'error'
                print(f"Error downloading {file_path}: {e}")
        else:
            print(f"File already exists, skipping: {file_path}")

    dataset_directory = "tmp/finance-bench"
    df_finbench.to_csv(os.path.join(dataset_directory, "finance_bench_dataset.csv"), index=False)
    print(f"All files processed. Total files downloaded: {count}")


if __name__ == "__main__":
    download_dataset()
