"""Abstract plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, TypeVar

from openssa.l2.reasoning.base import BaseReasoner

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.task.abstract import ATask


@dataclass
class AbstractPlan(ABC):
    """Abstract plan."""

    task: ATask

    sub_plans: list[Self] = field(default_factory=list,
                                  init=True,
                                  repr=True,
                                  hash=False,  # mutable
                                  compare=True,
                                  metadata=None,
                                  kw_only=True)

    @abstractmethod
    def execute(self, reasoner: AReasoner = BaseReasoner()) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
