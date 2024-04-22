"""Abstract planning classes."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, TypeVar

from openssa.l2.reasoning.base import BaseReasoner
from openssa.utils.llms import AnLLM, OpenAILLM

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.task.abstract import ATask


@dataclass
class AbstractPlan(ABC):
    """Abstract plan."""
    task: ATask

    @abstractmethod
    def execute(self, reasoner: AReasoner = BaseReasoner()) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)


@dataclass
class AbstractPlanner(ABC):
    """Abstract planner."""

    lm: AnLLM = field(default_factory=OpenAILLM.get_gpt_4_1106_preview)

    max_depth: int = 3
    max_subtasks_per_decomp: int = 3

    @abstractmethod
    def reduce_depth(self) -> Self:
        """Make 1-fewer-level-deep planner."""

    @abstractmethod
    def plan(self, problem: str, resources: set[AResource] | None = None) -> APlan:
        """Make plan for solving problem based on informational resources."""

    @abstractmethod
    def update_plan_resources(self, plan: APlan, /, resources: set[AResource]) -> APlan:
        """Make updated plan copy with relevant informational resources."""


APlanner: TypeVar = TypeVar('APlanner', bound=AbstractPlanner, covariant=False, contravariant=False)
