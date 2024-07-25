from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openssa.l2.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.l2.programming.abstract.program import AProgram
    from openssa.l2.util.lm.abstract import AnLM


@dataclass
class ProgramSpace:
    descriptions: dict[str, str] = field(default_factory=dict)
    programs: dict[str, AProgram] = field(default_factory=dict)

    lm: AnLM = field(default_factory=OpenAILM)

    def add_or_update_program(self, name: str, description: str, program: AProgram):
        """Add program to library with unique identifying name & informative description."""
        self.descriptions[name]: str = description
        self.programs[name]: AProgram = program

    def find_program(self, problem: str) -> AProgram:
        """Find program for problem."""
