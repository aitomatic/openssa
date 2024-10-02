from dotenv import load_dotenv
import os
from openssa import DANA, DbResource
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import yaml

load_dotenv()


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


config = load_yaml('db_config.yaml')
db_host = config['database']['mysql']['host']
db_database = config['database']['mysql']['database']
db_user = config['database']['mysql']['username']
db_password = config['database']['mysql']['password']
db_port = config['database']['mysql']['port']

openai_api_key = os.getenv('OPENAI_API_KEY')

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


def generate_sql_from_prompt(question) -> str:
    vn_openai = MyVanna(config={'model': 'gpt-4o', 'api_key': openai_api_key})
    vn_openai.connect_to_mysql(host=db_host, dbname=db_database, user=db_user, password=db_password, port=db_port)
    return vn_openai.generate_sql(question)


def get_or_create_agent(query) -> DANA:
    return DANA(
        # TODO: For Argument Use SQL first and use prompt later
        resources=[DbResource(config_path="db_config.yaml", query=query)]
    )


def solve(question, query) -> str:
    agent = get_or_create_agent(query)
    try:
        return agent.solve(problem=question)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return f'ERROR: {err}'


if __name__ == '__main__':
    QUESTION = (
        # TODO:ここを変更（プロンプト）
        # "Please tell me cheapest item from items table."
        "What is the best-selling product in the last year from sales_data table?"
    )

    query = generate_sql_from_prompt(QUESTION)
    answer = solve(QUESTION, query)

    # TODO: 出力情報の追加 (vanna aiで作成して使用されたSQLなど)
    print('--------------------------------')
    print(answer)
    print('--------------------------------')
    print(query)
    print('--------------------------------')
