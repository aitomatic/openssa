from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.neurosym.program.abstract import AbstractProgram
    from openssa.neurosym.program.program_space import ProgramSpace

    from openssa.l2.knowledge.abstract import Knowledge
    from openssa import AbstractResource, OodaReasoner


@dataclass
class Agent:
    """Neuro-Symbolic Problem-Solving Agent."""

    program_space: ProgramSpace

    knowledge: set[Knowledge] = field(default_factory=set)
    resources: set[AbstractResource] = field(default_factory=set)

    def solve(self, problem: str) -> str:
        """Solve problem."""
        program: AbstractProgram = self.program_space.find_program(problem=problem)
        return program.execute(inputs=self.resources)
