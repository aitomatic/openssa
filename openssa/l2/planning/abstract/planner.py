"""
===============================
ABSTRACT TASK PLANNER INTERFACE
===============================

`AbstractPlanner` is `OpenSSA`'s abstract base class for using LMs to create or update problem-solving task plans.

A planner has an LM for generating new or updated task plans,
the complexity of which is controlled by at least 2 key parameters `max_depth` and `max_subtasks_per_decomp`.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, TypeVar, TYPE_CHECKING

# from openssa.l2.util.lm.openai import OpenAILM
from openssa.l2.util.lm.huggingface_lm import HuggingFaceLM

if TYPE_CHECKING:
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.util.lm.abstract import AnLM
    from .plan import APlan


@dataclass
class AbstractPlanner(ABC):
    """Abstract Planner."""

    # language model for generating solution Plans
    # lm: AnLM = field(default_factory=OpenAILM.from_defaults,
    #                  init=True,
    #                  repr=True,
    #                  hash=None,
    #                  compare=True,
    #                  metadata=None,
    #                  kw_only=False)
    lm: AnLM = field(default_factory=HuggingFaceLM.from_defaults,
                     init=True,
                     repr=True,
                     hash=None,
                     compare=True,
                     metadata=None,
                     kw_only=False)

    # generally applicable parameters for controlling generated Plans' allowed complexity
    max_depth: int = 2
    max_subtasks_per_decomp: int = 3

    def one_level_deep(self) -> Self:
        """Get 1-level-deep Planner with same other parameters."""
        return type(self)(lm=self.lm, max_depth=1, max_subtasks_per_decomp=self.max_subtasks_per_decomp)

    def one_fewer_level_deep(self) -> Self:
        """Get 1-fewer-level-deep Planner with same other parameters."""
        return type(self)(lm=self.lm, max_depth=self.max_depth - 1, max_subtasks_per_decomp=self.max_subtasks_per_decomp)  # noqa: E501

    @abstractmethod
    def plan(self, problem: str, *, knowledge: set[Knowledge] | None = None, resources: set[AResource] | None = None) -> APlan:  # noqa: E501
        """Make Plan for solving posed Problem using given Knowledge & Informational Resources."""

    @abstractmethod
    def update_plan_resources(self, plan: APlan, /, problem: str, resources: set[AResource],
                              *, knowledge: set[Knowledge] | None = None) -> APlan:
        """Make updated Plan for solving posed Problem using given Knowledge & relevant Informational Resources."""


APlanner: TypeVar = TypeVar('APlanner', bound=AbstractPlanner, covariant=False, contravariant=False)
