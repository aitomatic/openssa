"""
====================
PROGRAMMER INTERFACE
====================

`BaseProgrammer` is `OpenSSA`'s abstract base class for using LMs to create problem-solving Programs.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from openssa.core.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.core.knowledge.base import Knowledge
    from openssa.core.task.task import Task
    from openssa.core.util.lm.base import BaseLM
    from .program import BaseProgram


@dataclass
class BaseProgrammer(ABC):
    """Programmer abstract base class."""

    # language model for generating problem-solving Programs
    lm: BaseLM = field(default_factory=OpenAILM.from_defaults,
                       init=True,
                       repr=True,
                       hash=None,
                       compare=True,
                       metadata=None,
                       kw_only=False)

    @abstractmethod
    def create_program(self, task: Task, knowledge: set[Knowledge] | None = None, **kwargs: Any) -> BaseProgram:
        """Construct a Program for solving the posed Problem using given Knowledge & Resources."""
