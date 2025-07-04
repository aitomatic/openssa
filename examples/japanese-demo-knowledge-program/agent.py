import yaml
from pathlib import Path
from loguru import logger
from functools import cache
from openssa import DANA, ProgramStore, HTP, HTPlanner
from openssa.core.util.lm.openai import OpenAILM
from openssa.core.programming.hierarchical.plan import HTPDict


EXPERT_KNOWLEDGE_PATH: Path = Path(__file__).parent / 'expert-knowledge.md'
EXPERT_PROGRAMS_PATH: Path = Path(__file__).parent / 'expert-programs.yml'


@cache
def get_expert_knowledge() -> str:
    try:
        with open(EXPERT_KNOWLEDGE_PATH, 'r') as f:
            EXPERT_KNOWLEDGE: str = f.read()
            return EXPERT_KNOWLEDGE
    except FileNotFoundError:
        logger.error(f'Expert knowledge file not found: {EXPERT_KNOWLEDGE_PATH}')
        return ''

@cache
def get_expert_programs() -> dict[str, HTPDict]:
    try:
        with open(EXPERT_PROGRAMS_PATH, 'r') as f:
            EXPERT_PROGRAMS: dict[str, HTPDict] = yaml.safe_load(stream=f)
            return EXPERT_PROGRAMS
    except FileNotFoundError:
        logger.error(f'Expert programs file not found: {EXPERT_PROGRAMS_PATH}')
        return {}

@cache
def get_or_create_agent() -> DANA:
    lm = OpenAILM.from_defaults()
    program_store = ProgramStore(lm=lm)
    expert_programs = get_expert_programs()
    expert_knowledge = get_expert_knowledge()
    if expert_programs:
        for program_name, htp_dict in expert_programs.items():
            htp = HTP.from_dict(htp_dict)
            program_store.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return DANA(
        program_store=program_store,
        programmer=HTPlanner(lm=lm, max_depth=2, max_subtasks_per_decomp=4),
        knowledge={expert_knowledge} if expert_knowledge else None,
        resources={}
    )



