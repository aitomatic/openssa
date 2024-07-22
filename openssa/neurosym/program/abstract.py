from __future__ import annotations

from abc import ABC, abstractmethod


type ProgramIO = dict | list | str


class AbstractProgram(ABC):
    @abstractmethod
    def execute(self, inputs: ProgramIO) -> ProgramIO:
        """Execute on given inputs and return outputs."""
