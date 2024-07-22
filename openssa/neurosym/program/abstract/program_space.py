from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.neurosym.program.abstract.program import AbstractProgram


class AbstractProgramSpace(ABC):
    @abstractmethod
    def add_program(self, name: str, desc: str, program: AbstractProgram):
        """Add program to library with unique identifying name & informative description."""
