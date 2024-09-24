"""
Reads stored answers and maps them to keyword in question
"""

keyword_file_map = {}

keyword_file_map['ragweed'] = 'ans_1'
keyword_file_map['foxtail'] = 'ans_1_1'
keyword_file_map['biosolids'] = "ans_2"
keyword_file_map['hyperspectral'] = "ans_3"
keyword_file_map['cutworm'] = 'ans_4'

qa_map = {}

for keyword, filename in keyword_file_map.items():
    with open(f'./answer_files/{filename}.md', encoding='utf-8') as file:
        retrieved_content = file.read()
    qa_map[keyword] = retrieved_content
