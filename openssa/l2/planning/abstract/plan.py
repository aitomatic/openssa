"""Abstract Plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self, TypeVar, TypedDict, Required, NotRequired, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task.abstract import ATask


type AskAnsPair = tuple[str, str]


class PlanQuickRepr(TypedDict):
    task: Required[str]
    sub_plans: NotRequired[list[Self]]


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
    def quick_repr(self) -> PlanQuickRepr:
        d: PlanQuickRepr = {'task': self.task.ask}

        if self.sub_plans:
            d['sub-plans']: list[PlanQuickRepr] = [sub_plan.quick_repr for sub_plan in self.sub_plans]

        return d

    @abstractmethod
    def execute(self, reasoner: AReasoner, knowledge: set[Knowledge] | None = None,
                other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified Reasoner and Knowledge to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
