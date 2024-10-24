from pathlib import Path
from dotenv import load_dotenv
from openssa import DANA, FileResource

load_dotenv()

DOCS_DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'


def get_or_create_agent() -> DANA:
    return DANA(
        resources={FileResource(path=DOCS_DATA_LOCAL_DIR_PATH)}
    )


def solve(question) -> str:
    agent = get_or_create_agent()
    try:
        return agent.solve(problem=question)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return f'ERROR: {err}'


if __name__ == '__main__':
    QUESTION = (
        'Please tell me three dishes you recommend.'
        'Please limit the total salt content of the three dishes to less than 21.5g.'
        'Also, please make sure that the total amount of vegetables in the three dishes is at least 700g.'
        'Please answer in Japanese.'
    )
    answer = solve(QUESTION)

    print('--------------------------------')
    print(answer)
    print('--------------------------------')
