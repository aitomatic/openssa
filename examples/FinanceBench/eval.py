import os
import argparse
import pandas as pd
import yaml
from dotenv import load_dotenv, find_dotenv

from openai import OpenAI
from openssa.utils.llms import OpenAILLM

def read_csv_file(file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        print("CSV file successfully read:")
        print(df.head())
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error occurred while reading CSV file: {e}")
        return None
    
def read_yaml_file(yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {yaml_file_path}")
        return None
    except Exception as e:
        print(f"Error occurred while reading YAML file: {e}")
        return None


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process YAML and CSV file paths.")
    parser.add_argument("--yaml_file_path", type=str, default="/home/shruti/AITOMATIC/source_code/other_scripts/auto_eval_script/ground-truths.yml",
                        help="Path to the YAML file (default: %(default)s)")
    parser.add_argument("--csv_file_path", type=str, default="/home/shruti/AITOMATIC/source_code/other_scripts/auto_eval_script/output.csv",
                        help="Path to the CSV file (default: %(default)s)")
    parser.add_argument("--ID_col", type=str, default="financebench_id",
                        help="Name of the column containing IDs (default: %(default)s)")
    parser.add_argument("--answer_col", type=str, default="OODA",
                        help="Name of the column containing answers (default: %(default)s)")
    parser.add_argument("--financebench_id", type=str, default="financebench_id_00222",
                        help="Financebench ID (default: %(default)s)")
    
    return parser.parse_args()

def get_eval_prompt(financebench_id, reference_data, generated_data, ID_col, answer_col):
    
    question = reference_data[financebench_id]['question']
    rubric = reference_data[financebench_id]['correctness']
    answer = generated_data[generated_data[ID_col] == financebench_id][answer_col].item()
    
    prompt = f"You are an objective and precise assistant. \
              Evaluate whether the answer generated is correct according to the grading criterion described in the RUBRIC. \
              Output only a single word. Say YES if you judge the answer to be correct, and NO if incorrect.\
              question: {question}\
              answer: {answer} \
              rubric: {rubric}"
    return prompt
    

def create_LLM(model = "gpt-4-1106-preview"):
    
    _ = load_dotenv(find_dotenv())
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

    llm = OpenAILLM(model=model, api_key=OPENAI_API_KEY)
    return llm

def evaluate_question(financebench_id, reference_data, generated_data, ID_col, answer_col): 
    
    Prompt = get_eval_prompt(financebench_id, reference_data, generated_data, ID_col, answer_col)
    
    llm = create_LLM()

    response = llm.get_response(prompt=Prompt)
    return response


def main(): 
    args = parse_arguments()

    yaml_file_path = args.yaml_file_path
    csv_file_path = args.csv_file_path
    ID_col = args.ID_col
    answer_col = args.answer_col
    financebench_id = args.financebench_id

    reference_data = read_yaml_file(yaml_file_path)
    generated_data = read_csv_file(csv_file_path)

    if financebench_id == "all": 
        for id in generated_data[ID_col]:
            score = evaluate_question(id, reference_data, generated_data, ID_col, answer_col)
            #store score in csv
            print(score)

    else: 
        score = evaluate_question(financebench_id, reference_data, generated_data, ID_col, answer_col)
        print(score)
        

if __name__ == "__main__":
    main()