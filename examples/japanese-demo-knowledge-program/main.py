from pathlib import Path
from functools import cache
from dotenv import load_dotenv
from openssa import DANA, FileResource, ProgramStore, HTPlanner
from openssa.core.util.lm.openai import OpenAILM
from argparse import ArgumentParser

load_dotenv()

DOCS_DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'


@cache
def get_main_lm():
    return OpenAILM.from_defaults()


@cache
def get_or_create_program_store() -> ProgramStore:
    # Optionally create and configure a ProgramStore
    return ProgramStore()


@cache
def get_or_create_agent(use_knowledge: bool = False, use_program_store: bool = False) -> DANA:
    # Instantiate DANA with optional knowledge and program store
    knowledge = None if not use_knowledge else {"KnowledgeBase"}
    program_store = get_or_create_program_store() if use_program_store else ProgramStore()

    return DANA(
        knowledge=knowledge,
        program_store=program_store,
        programmer=HTPlanner(lm=get_main_lm(), max_depth=3, max_subtasks_per_decomp=6),
        resources={FileResource(path=DOCS_DATA_LOCAL_DIR_PATH)}
    )


def solve(question: str, use_knowledge: bool, use_program_store: bool) -> str:
    agent = get_or_create_agent(use_knowledge=use_knowledge, use_program_store=use_program_store)
    try:
        return agent.solve(problem=question)
    except Exception as err:
        return f'ERROR: {err}'


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--knowledge', action='store_true', help="Use expert knowledge")
    arg_parser.add_argument('--prog-store', action='store_true', help="Use expert program store")
    args = arg_parser.parse_args()

    QUESTION = (
        'Please tell me three dishes you recommend. '
        'Please limit the total salt content of the three dishes to less than 21.5g. '
        'Also, please make sure that the total amount of vegetables in the three dishes is at least 700g. '
        'Please answer in Japanese.'
    )
    answer = solve(QUESTION, use_knowledge=args.knowledge, use_program_store=args.prog_store)

    print('--------------------------------')
    print(answer)
    print('--------------------------------')
