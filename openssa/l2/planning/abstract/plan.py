"""Abstract Plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, TypedDict, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.task.abstract import ATask


type AskAnsPair = tuple[str, str]


class PlanQuickRepr(TypedDict):
    task: str
    sub_plans: list[Self]


@dataclass
class AbstractPlan(ABC):
    """Abstract Plan."""

    # target Task to solve
    task: ATask

    # decomposed Sub-Plans for solving target Task
    sub_plans: list[Self] = field(default_factory=list)

    @property
    def quick_repr(self) -> PlanQuickRepr:
        return {'task': self.task.ask,
                'sub-plans': [sub_plan.quick_repr for sub_plan in self.sub_plans]}

    @abstractmethod
    def execute(self, reasoner: AReasoner, other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
