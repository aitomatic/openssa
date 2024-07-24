"""
==========================
ABSTRACT PROGRAM INTERFACE
==========================

`AbstractProgram` is `OpenSSA`'s abstract base class for problem-solving programs.

A program has a target `task` to solve, and can contain decomposed `sub_programs` for solving that `task`.

A program can be executed through its own `.execute(...)` method,
by a specified Reasoner that optionally takes into account some given domain-specific Knowledge and/or other results.
The program execution returns a string result.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pprint import pformat
from types import SimpleNamespace
from typing import Any, Self, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task import Task
    from openssa.l2.util.misc import AskAnsPair


class PLAN(SimpleNamespace):
    pass  # namespace class just for pretty-printing


@dataclass
class AbstractProgram(ABC):
    """Abstract Program."""

    # target Task to solve
    task: Task

    # decomposed Sub-Plans for solving target Task
    sub_programs: list[Self] = field(default_factory=list,
                                     init=True,
                                     repr=True,
                                     hash=None,
                                     compare=True,
                                     metadata=None,
                                     kw_only=False)

    def concretize_tasks_from_template(self, **kwargs: Any):
        self.task.ask: str = self.task.ask.format(**kwargs)

        for sub_program in self.sub_programs:
            sub_program.concretize_tasks_from_template(**kwargs)

    @property
    def quick_repr(self) -> PLAN:
        """Quick, pretty-formattable/printable namespace representation."""
        namespace: PLAN = PLAN(task=self.task.ask)

        if self.sub_programs:
            namespace.subs: list[PLAN] = [sub_program.quick_repr for sub_program in self.sub_programs]

        return namespace

    @property
    def pformat(self) -> str:
        """Pretty-formatted string representation."""
        return pformat(object=self.quick_repr,
                       indent=2,
                       width=120,
                       depth=None,
                       compact=False,
                       sort_dicts=False,
                       underscore_numbers=False).replace("'", '').replace('\\n', '')

    @abstractmethod
    def execute(self, reasoner: AReasoner, knowledge: set[Knowledge] | None = None,
                other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return string result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account domain-specific Knowledge and/or potentially elevant other results.
        """


AProgram: TypeVar = TypeVar('AProgram', bound=AbstractProgram, covariant=False, contravariant=False)
