from __future__ import annotations

from argparse import ArgumentParser
from functools import cache

from openssa import Agent, ProgramSpace, HTP, HTPlanner, OpenAILM

# pylint: disable=wrong-import-order
from data_and_knowledge import EXPERT_PROGRAM_SPACE, EXPERT_KNOWLEDGE
from semikong_lm import SemiKongLM


@cache
def get_or_create_agent(use_semikong_lm: bool = True, max_depth=2, max_subtasks_per_decomp=4) -> Agent:
    lm = (SemiKongLM if use_semikong_lm else OpenAILM).from_defaults()

    program_space = ProgramSpace(lm=lm)
    if EXPERT_PROGRAM_SPACE:
        for program_name, htp_dict in EXPERT_PROGRAM_SPACE.items():
            htp = HTP.from_dict(htp_dict)
            program_space.add_or_update_program(name=program_name, description=htp.task.ask, program=htp)

    return Agent(program_space=program_space,
                 programmer=HTPlanner(lm=lm, max_depth=max_depth, max_subtasks_per_decomp=max_subtasks_per_decomp),
                 knowledge={EXPERT_KNOWLEDGE} if EXPERT_KNOWLEDGE else None,
                 resources={})


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('problem')
    args = arg_parser.parse_args()

    print(get_or_create_agent().solve(problem=args.problem))
