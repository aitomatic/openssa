"""Abstract planning classes."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openssa.l2.reasoning.base import BaseReasoner
from openssa.utils.llms import AnLLM, OpenAILLM

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AbstractReasoner
    from openssa.l2.resource.abstract import AbstractResource
    from openssa.l2.task.task import Task


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=False,  # mutable
           match_args=True,
           kw_only=False,
           slots=False,
           weakref_slot=False)
class AbstractPlan(ABC):
    """Abstract plan."""
    task: Task

    @abstractmethod
    def execute(self, reasoner: AbstractReasoner = BaseReasoner()) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=False,  # mutable
           match_args=True,
           kw_only=False,
           slots=False,
           weakref_slot=False)
class AbstractPlanner(ABC):
    """Abstract planner."""

    lm: AnLLM = field(default_factory=OpenAILLM.get_gpt_4_1106_preview)

    @abstractmethod
    def plan(self, problem: str, resources: set[AbstractResource] | None = None) -> AbstractPlan:
        """Make plan for solving problem based on informational resources."""

    @abstractmethod
    def update_plan_resources(self, plan: AbstractPlan, /, resources: set[AbstractResource]) -> AbstractPlan:
        """Make updated plan copy with relevant informational resources."""
