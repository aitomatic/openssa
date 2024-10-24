from __future__ import annotations

from argparse import ArgumentParser
from functools import cache

# pylint: disable=wrong-import-order
from data_and_knowledge import EXPERT_PROGRAMS, EXPERT_KNOWLEDGE
from openssa import DANA, ProgramStore, HTP, HTPlanner, OpenAILM
from semikong_lm import SemiKongLM


@cache
def get_or_create_agent(use_semikong_lm: bool = True, max_depth=2, max_subtasks_per_decomp=4) -> DANA:
    lm = (SemiKongLM if use_semikong_lm else OpenAILM).from_defaults()

    program_store = ProgramStore(lm=lm)
    if EXPERT_PROGRAMS:
        for program_name, htp_dict in EXPERT_PROGRAMS.items():
            htp = HTP.from_dict(htp_dict)
            program_store.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return DANA(program_store=program_store,
                programmer=HTPlanner(lm=lm, max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp),
                knowledge={EXPERT_KNOWLEDGE} if EXPERT_KNOWLEDGE else None,
                resources={})


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('problem')
    args = arg_parser.parse_args()

    print(get_or_create_agent().solve(problem=args.problem))
