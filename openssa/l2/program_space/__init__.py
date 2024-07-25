from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import TYPE_CHECKING

from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.util.lm.openai import OpenAILM

from ._prompts import PROGRAM_SEARCH_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.programming.abstract.program import AProgram
    from openssa.l2.util.lm.abstract import AnLM, LMChatHist


@dataclass
class ProgramSpace:
    descriptions: dict[str, str] = field(default_factory=dict)
    programs: dict[str, AProgram] = field(default_factory=dict)

    lm: AnLM = field(default_factory=OpenAILM)

    def add_or_update_program(self, name: str, description: str, program: AProgram):
        """Add program to library with unique identifying name & informative description."""
        self.descriptions[name]: str = description
        self.programs[name]: AProgram = program

    def find_program(self, problem: str, knowledge: set[Knowledge] | None = None) -> AProgram | None:
        """Find program for problem."""
        knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                if knowledge
                                                else None)

        matching_program_name: str = self.lm.get_response(
            prompt=PROGRAM_SEARCH_PROMPT_TEMPLATE.format(problem=problem,
                                                         program_descriptions=json.dumps(self.descriptions)),
            history=knowledge_lm_hist)

        if matching_program_name.startswith('NONE'):
            return None

        return self.programs[matching_program_name]
