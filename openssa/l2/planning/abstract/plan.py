"""Abstract Plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, TypeVar, TypedDict, Required, NotRequired, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
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
    sub_plans: list[Self] = field(default_factory=list)

    @property
    def quick_repr(self) -> PlanQuickRepr:
        d: PlanQuickRepr = {'task': self.task.ask}

        if self.sub_plans:
            d['sub-plans']: list[PlanQuickRepr] = [sub_plan.quick_repr for sub_plan in self.sub_plans]

        return d

    @abstractmethod
    def execute(self, reasoner: AReasoner, other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
