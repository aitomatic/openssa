"""Abstract Plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, TypeVar

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.task.abstract import ATask


type AskAnsPair = tuple[str, str]


@dataclass
class AbstractPlan(ABC):
    """Abstract Plan."""

    # target Task to solve
    task: ATask

    # decomposed Sub-Plans for solving target Task
    sub_plans: list[Self] = field(default_factory=list)

    @abstractmethod
    def execute(self, reasoner: AReasoner, knowledge: set[str] = None, other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
