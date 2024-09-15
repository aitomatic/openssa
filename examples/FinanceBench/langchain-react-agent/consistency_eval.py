# import openai
# import pandas as pd
# import os
# import sys
# from concurrent.futures import ThreadPoolExecutor, as_completed

# if len(sys.argv) != 2:
#     print("Usage: python script_name.py <path_to_csv_file>")
#     sys.exit(1)

# csv_file_path = sys.argv[1]
# df = pd.read_csv(csv_file_path)

# MODEL = "gpt-4o"
# client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# consistency_columns = [
#     'consistent_1_2', 'consistent_1_3', 'consistent_1_4', 
#     'consistent_2_3', 'consistent_2_4', 
#     'consistent_3_4'
# ]

# df[consistency_columns] = None
# df['score'] = None

# def get_consistency_results(prompt):
#     completion = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     response = completion.choices[0].message.content
#     return response

# def process_row(index, row):
#     prompt = f"""Question: {row['question']}

# Answer 1: {row['answer 1']}
# Answer 2: {row['answer 2']}
# Answer 3: {row['answer 3']}
# Answer 4: {row['answer 4']}

# Now, please help me compare the consistency of pairwise answers. I have 4 answers above, so please create a combination of 2 over 4 answers. Should be 6 pairs. Help me do these 2 tasks:

# 1. Justify the consistency of two answers. If the equivalent values are exactly the same, that's perfect. If the difference is not significant (less than 10%), that's ok, but give some penalty. If the difference is significant (more than 10%), that's bad.
# 2. Let me know if they are consistent, 1 if yes, 0 if no, and 0.5 if the difference is not significant.

# Your answer should follow this format:
# justification_1_2: justification for answer 1 and answer 2
# consistent_1_2: 1 if answers 1 and 2 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
# justification_1_3: justification for answer 1 and answer 3
# consistent_1_3: 1 if answers 1 and 3 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
# justification_1_4: justification for answer 1 and answer 4
# consistent_1_4: 1 if answers 1 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
# justification_2_3: justification for answer 2 and answer 3
# consistent_2_3: 1 if answers 2 and 3 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
# justification_2_4: justification for answer 2 and answer 4
# consistent_2_4: 1 if answers 2 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
# justification_3_4: justification for answer 3 and answer 4
# consistent_3_4: 1 if answers 3 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.

# Do not forget the key and do not change the key format. Thank you!
# """
#     while True:
#         response = get_consistency_results(prompt)
#         try:
#             result = {column: float(response.split(f'{column}: ')[1].split('\n')[0].strip()) for column in consistency_columns}
#             break
#         except (IndexError, ValueError) as e:
#             print(f"Error processing row {index + 1}: {e}. Retrying...")

#     result['score'] = pd.Series(result).mean()
#     print(f"Average consistency score for row {index + 1}: {result['score']}")
#     return index, result

# with ThreadPoolExecutor() as executor:
#     futures = [executor.submit(process_row, index, row) for index, row in df.iterrows()]
    
#     for future in as_completed(futures):
#         index, result = future.result()
#         df.loc[index, consistency_columns + ['score']] = result.values()

# final_consistency_score = df['score'].mean()
# print(f"Final consistency score: {final_consistency_score}")

# output_file = 'langchain-react-consistency-4.csv'
# df.to_csv(output_file, index=False)

# print(f"Processing complete and file saved as {output_file}.")


import openai
import pandas as pd
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

if len(sys.argv) != 2:
    print("Usage: python script_name.py <path_to_csv_file>")
    sys.exit(1)

csv_file_path = sys.argv[1]
df = pd.read_csv(csv_file_path)

MODEL = "gpt-4o"
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Updating for 5 answers (10 pairwise combinations)
consistency_columns = [
    'consistent_1_2', 'consistent_1_3', 'consistent_1_4', 'consistent_1_5',
    'consistent_2_3', 'consistent_2_4', 'consistent_2_5',
    'consistent_3_4', 'consistent_3_5',
    'consistent_4_5'
]

df[consistency_columns] = None
df['score'] = None

def get_consistency_results(prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response

def process_row(index, row):
    prompt = f"""Question: {row['question']}

Answer 1: {row['answer 1']}
Answer 2: {row['answer 2']}
Answer 3: {row['answer 3']}
Answer 4: {row['answer 4']}
Answer 5: {row['answer 5']}

Now, please help me compare the consistency of pairwise answers. I have 5 answers above, so please create a combination of 2 over 5 answers. Should be 10 pairs. Help me do these 2 tasks:

1. Justify the consistency of two answers. If the equivalent values are exactly the same, that's perfect. If the difference is not significant (less than 10%), that's ok, but give some penalty. If the difference is significant (more than 10%), that's bad.
2. Let me know if they are consistent, 1 if yes, 0 if no, and 0.5 if the difference is not significant.

Your answer should follow this format:
justification_1_2: justification for answer 1 and answer 2
consistent_1_2: 1 if answers 1 and 2 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_1_3: justification for answer 1 and answer 3
consistent_1_3: 1 if answers 1 and 3 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_1_4: justification for answer 1 and answer 4
consistent_1_4: 1 if answers 1 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_1_5: justification for answer 1 and answer 5
consistent_1_5: 1 if answers 1 and 5 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_2_3: justification for answer 2 and answer 3
consistent_2_3: 1 if answers 2 and 3 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_2_4: justification for answer 2 and answer 4
consistent_2_4: 1 if answers 2 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_2_5: justification for answer 2 and answer 5
consistent_2_5: 1 if answers 2 and 5 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_3_4: justification for answer 3 and answer 4
consistent_3_4: 1 if answers 3 and 4 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_3_5: justification for answer 3 and answer 5
consistent_3_5: 1 if answers 3 and 5 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.
justification_4_5: justification for answer 4 and answer 5
consistent_4_5: 1 if answers 4 and 5 are consistent, 0 if they are inconsistent, 0.5 if the difference is not significant.

Do not forget the key and do not change the key format. Thank you!
"""
    while True:
        response = get_consistency_results(prompt)
        try:
            result = {column: float(response.split(f'{column}: ')[1].split('\n')[0].strip()) for column in consistency_columns}
            break
        except (IndexError, ValueError) as e:
            print(f"Error processing row {index + 1}: {e}. Retrying...")

    result['score'] = pd.Series(result).mean()
    print(f"Average consistency score for row {index + 1}: {result['score']}")
    return index, result

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_row, index, row) for index, row in df.iterrows()]
    
    for future in as_completed(futures):
        index, result = future.result()
        df.loc[index, consistency_columns + ['score']] = result.values()

final_consistency_score = df['score'].mean()
print(f"Final consistency score: {final_consistency_score}")

output_file = 'langchain-react-consistency-5.csv'
df.to_csv(output_file, index=True)

print(f"Processing complete and file saved as {output_file}.")
