from pathlib import Path
from dotenv import load_dotenv
from openssa import DANA, DbResource

load_dotenv()

# いらなそう
LOCAL_CACHE_DOCS_DIR_PATH: Path = Path(__file__).parent / '.data'


def get_or_create_agent() -> DANA:
    return DANA(
        # TODO: For Argument Use SQL first and use prompt later
        resources=[DbResource(config_path="db_config.yaml", query="SELECT * FROM items")]
    )


def solve(question) -> str:
    agent = get_or_create_agent()
    try:
        return agent.solve(problem=question)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return f'ERROR: {err}'


if __name__ == '__main__':
    QUESTION = (
        # TODO:ここを変更（プロンプト）
        'Please tell me cheapest item from items table.'
        'Please answer in Japanese.'
    )
    answer = solve(QUESTION)

# TODO: 出力情報の追加 (作成して使用されたSQLなど)
    print('--------------------------------')
    print(answer)
    print('--------------------------------')
