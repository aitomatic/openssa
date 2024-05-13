from pathlib import Path
from dotenv import load_dotenv
from openssa import OodaSSA, TaskDecompositionHeuristic


load_dotenv()


LOCAL_CACHE_DOCS_DIR_PATH: Path = Path(__file__).parent / '.data'
JAPANESE_DEMO_HEURISTICS: str = (
    'Please answer in Japanese.'
    'Pay attention to the total salt content, calories, and total vegetables.'
)


def get_or_create_ooda_ssa() -> OodaSSA:
    ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                  highest_priority_heuristic=JAPANESE_DEMO_HEURISTICS,
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
    QUESTION = (
        'Please tell me three dishes you recommend.'
        'Please limit the total salt content of the three dishes to less than 21.5g.'
        'Also, please make sure that the total amount of vegetables in the three dishes is at least 700g.'
    )
    answer = solve(QUESTION)

    print('--------------------------------')
    print(answer)
    print('--------------------------------')
