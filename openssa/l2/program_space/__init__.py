from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.neurosym.program.abstract import AbstractProgram


class ProgramSpace:
    def add_program(self, name: str, desc: str, program: AbstractProgram):
        """Add program to library with unique identifying name & informative description."""

    def find_program(self, problem: str) -> AbstractProgram:
        """Find program for problem."""
