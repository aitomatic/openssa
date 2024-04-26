from pathlib import Path
from dotenv import load_dotenv
from openssa import OodaSSA, TaskDecompositionHeuristic


load_dotenv()


LOCAL_CACHE_DOCS_DIR_PATH: Path = Path(__file__).parent / '.data'
THREE_FIN_STATEMENTS_HEURISTICS: str = (
    '日本語で回答してください。'
)


def get_or_create_ooda_ssa() -> OodaSSA:
    ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                  highest_priority_heuristic=THREE_FIN_STATEMENTS_HEURISTICS,
                  enable_generative=True)
    ssa.activate_resources(LOCAL_CACHE_DOCS_DIR_PATH)
    return ssa


def solve(question) -> str:
    ooda_ssa = get_or_create_ooda_ssa()
    try:
        return ooda_ssa.solve(question)

    except Exception as err:  # pylint: disable=broad-exception-caught
        return f'ERROR: {err}'


if __name__ == '__main__':
    question = 'じゅんさい鍋と石狩鍋どちらがおすすめですか。塩分とカロリーを抑えて出来るだけ野菜を摂取したいです。'
    answer = solve(question)

    print('--------------------------------')
    print(answer)
    print('--------------------------------')
