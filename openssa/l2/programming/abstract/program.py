"""
==========================
ABSTRACT PROGRAM INTERFACE
==========================

`AbstractProgram` is `OpenSSA`'s abstract base class for problem-solving Programs.

A Program has a target Task,
which encapsulates a posed Problem to solve and a set of Resources to help solve it.

A Program can be executed through its own `.execute(...)` method,
which optionally takes into account some given domain-specific Knowledge,
and which returns a string result.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task import Task


@dataclass
class AbstractProgram(ABC):
    """Abstract Program."""

    # target Task to solve
    task: Task

    @abstractmethod
    def execute(self, knowledge: set[Knowledge] | None = None, **kwargs: Any) -> str:
        """Execute and return string result.

        Execution also optionally takes into account domain-specific Knowledge.
        """


AProgram: TypeVar = TypeVar('AProgram', bound=AbstractProgram, covariant=False, contravariant=False)
