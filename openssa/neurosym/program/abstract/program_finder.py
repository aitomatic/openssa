from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.util.lm.abstract import AnLM
    from openssa.neurosym.program.abstract.program import AbstractProgram
    from openssa.neurosym.program.abstract.program_space import AbstractProgramSpace


@dataclass
class AbstractProgramFinder(ABC):
    lm: AnLM

    @abstractmethod
    def find_algo(self, problem: str, program_space: AbstractProgramSpace | None = None) -> AbstractProgram:
        """Find algorithm for problem."""
