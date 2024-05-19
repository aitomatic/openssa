"""Abstract Plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pprint import pformat
import re
from types import SimpleNamespace
from typing import Any, Self, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task.abstract import ATask
    from openssa.l2.util.misc import AskAnsPair


class PLAN(SimpleNamespace):
    """Plan Repr."""


@dataclass
class AbstractPlan(ABC):
    """Abstract Plan."""

    # target Task to solve
    task: ATask

    # decomposed Sub-Plans for solving target Task
    sub_plans: list[Self] = field(default_factory=list,
                                  init=True,
                                  repr=True,
                                  hash=None,
                                  compare=True,
                                  metadata=None,
                                  kw_only=False)

    def concretize_tasks_from_template(self, **kwargs: Any):
        self.task.ask: str = self.task.ask.format(**kwargs)

        for sub_plan in self.sub_plans:
            sub_plan.concretize_tasks_from_template(**kwargs)

    @property
    def quick_repr(self) -> PLAN:
        namespace: PLAN = PLAN(task=self.task.ask)

        if self.sub_plans:
            namespace.subs: list[PLAN] = [sub_plan.quick_repr for sub_plan in self.sub_plans]

        return namespace

    @property
    def pformat(self) -> str:
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
        """Execute and return result, using specified Reasoner and Knowledge to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
