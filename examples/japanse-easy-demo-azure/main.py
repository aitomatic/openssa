from pathlib import Path
from functools import cache
from dotenv import load_dotenv
from openssa import DANA, FileResource, HTPlanner
from lm.azure_program_store import ProgramStore
from lm.azure_openai import AzureOpenAILM
from lm.azure_llama_index import azure_llama_index_lm, azure_llama_index_embedding
from argparse import ArgumentParser

load_dotenv()

DOCS_DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'


@cache
def get_main_lm():
    return AzureOpenAILM.from_defaults()


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
        programmer=HTPlanner(lm=get_main_lm(), max_depth=1, max_subtasks_per_decomp=1),
        resources={FileResource(
            path=DOCS_DATA_LOCAL_DIR_PATH,
            lm=azure_llama_index_lm,
            embed_model=azure_llama_index_embedding)}
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
