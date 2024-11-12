from pathlib import Path
from functools import cache
from dotenv import load_dotenv
from openssa import DANA, FileResource, ProgramStore, HTPlanner
from openssa.core.util.lm.openai import OpenAILM
from fastapi import FastAPI, Query
from pydantic import BaseModel

load_dotenv()

DOCS_DATA_LOCAL_DIR_PATH: Path = Path(__file__).parent / '.data'
app = FastAPI()


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


class QuestionRequest(BaseModel):
    question: str
    use_knowledge: bool = False
    use_program_store: bool = False


@app.post("/solve")
async def solve_question(request: QuestionRequest):
    answer = solve(request.question, use_knowledge=request.use_knowledge, use_program_store=request.use_program_store)
    return {"answer": answer}
