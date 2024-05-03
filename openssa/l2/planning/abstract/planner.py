"""Abstract Planner."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, TypeVar

from openssa.l2.llms import AnLLM, OpenAILLM

if TYPE_CHECKING:
    from openssa.l2.resource.abstract import AResource
    from .plan import APlan


@dataclass
class AbstractPlanner(ABC):
    """Abstract Planner."""

    # language model for generating solution Plans
    lm: AnLLM = field(default_factory=OpenAILLM.from_defaults)

    # generally applicable parameters for controlling generated Plans' allowed complexity
    max_depth: int = 2
    max_subtasks_per_decomp: int = 3

    def one_level_deep(self) -> Self:
        """Get 1-level-deep Planner."""
        return type(self)(lm=self.lm, max_depth=1, max_subtasks_per_decomp=self.max_subtasks_per_decomp)

    def one_fewer_level_deep(self) -> Self:
        """Get 1-fewer-level-deep Planner."""
        return type(self)(lm=self.lm, max_depth=self.max_depth - 1, max_subtasks_per_decomp=self.max_subtasks_per_decomp)  # noqa: E501

    @abstractmethod
    def plan(self, problem: str, resources: set[AResource] | None = None) -> APlan:
        """Make Plan for solving posed Problem using Informational Resources."""

    @abstractmethod
    def update_plan_resources(self, plan: APlan, /, problem: str, resources: set[AResource]) -> APlan:
        """Make updated Plan for solving posed Problem using relevant Informational Resources."""


APlanner: TypeVar = TypeVar('APlanner', bound=AbstractPlanner, covariant=False, contravariant=False)
