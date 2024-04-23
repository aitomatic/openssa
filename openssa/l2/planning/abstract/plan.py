"""Abstract plan."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

from openssa.l2.reasoning.base import BaseReasoner

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.task.abstract import ATask


@dataclass
class AbstractPlan(ABC):
    """Abstract plan."""
    task: ATask

    @abstractmethod
    def execute(self, reasoner: AReasoner = BaseReasoner()) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""


APlan: TypeVar = TypeVar('APlan', bound=AbstractPlan, covariant=False, contravariant=False)
