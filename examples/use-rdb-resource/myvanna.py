from dotenv import load_dotenv
import os
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

# .envファイルの読み込み
load_dotenv()

# 環境変数から接続情報を取得
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_database = os.getenv('DB_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')

# MyVannaクラス定義
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

# sales_dataに基づいてVannaを訓練する関数
def train_vanna_for_sales_data(ddl):
    vn_openai = MyVanna(config={'model': 'gpt-4o', 'api_key': openai_api_key})
    vn_openai.train(ddl=ddl)

# プロンプトからSQLを生成する関数
def generate_sql_from_prompt(question) -> str:
    vn_openai = MyVanna(config={'model': 'gpt-4o', 'api_key': openai_api_key})
    vn_openai.connect_to_mysql(host=db_host, dbname=db_database, user=db_user, password=db_password, port=db_port)
    return vn_openai.generate_sql(question)
