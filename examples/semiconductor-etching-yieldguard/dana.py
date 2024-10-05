from __future__ import annotations

from argparse import ArgumentParser
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
import yaml

from openssa import DANA, ProgramStore, HTP, HTPlanner, HuggingFaceLM

# pylint: disable=wrong-import-order
from semikong_lm import SemiKongLM

if TYPE_CHECKING:
    from openssa.core.programming.hierarchical.plan import HTPDict


load_dotenv()


EXPERT_KNOWLEDGE_FILE_PATH: Path = Path(__file__).parent / 'expert-knowledge.txt'
with open(file=EXPERT_KNOWLEDGE_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_KNOWLEDGE: str = f.read()


EXPERT_PROGRAMS_FILE_PATH: Path = Path(__file__).parent / 'expert-programs.yml'
with open(file=EXPERT_PROGRAMS_FILE_PATH,
          buffering=-1,
          encoding='utf-8',
          errors='strict',
          newline=None,
          closefd=True,
          opener=None) as f:
    EXPERT_PROGRAMS: dict[str, HTPDict] = yaml.safe_load(stream=f)


@cache
def get_or_create_dana(use_semikong_lm: bool = False, max_depth=2, max_subtasks_per_decomp=4) -> DANA:
    lm = (SemiKongLM if use_semikong_lm else HuggingFaceLM).from_defaults()

    program_store = ProgramStore(lm=lm)
    if EXPERT_PROGRAMS:
        for program_name, htp_dict in EXPERT_PROGRAMS.items():
            htp = HTP.from_dict(htp_dict)
            program_store.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return DANA(knowledge={EXPERT_KNOWLEDGE},
                program_store=program_store,
                programmer=HTPlanner(lm=lm, max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp),
                resources={})


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('problem')
    args = arg_parser.parse_args()

    print(get_or_create_dana().solve(problem=args.problem))
