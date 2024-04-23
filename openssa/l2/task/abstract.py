"""Abstract task."""


from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, asdict, field
from typing import TYPE_CHECKING, Self, TypedDict, Required, NotRequired, TypeVar

from openssa.l2.planning.abstract.planner import AbstractPlanner
from openssa.l2.resource._global import GLOBAL_RESOURCES

from .status import TaskStatus

if TYPE_CHECKING:
    from openssa.l2.planning.abstract.plan import APlan
    from openssa.l2.planning.abstract.planner import APlanner
    from openssa.l2.resource.abstract import AResource


class TaskDict(TypedDict, total=False):
    ask: Required[str]
    resources: NotRequired[set[AResource]]
    status: NotRequired[TaskStatus]
    result: NotRequired[str]
    dynamic_decomposer: NotRequired[APlanner]


@dataclass
class AbstractTask(ABC):
    """Abstract task."""

    ask: str
    resources: set[AResource] = field(default_factory=set,
                                      init=True,
                                      repr=True,
                                      hash=False,  # mutable
                                      compare=True,
                                      metadata=None,
                                      kw_only=True)
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None
    dynamic_decomposer: APlanner | None = None

    @classmethod
    def from_dict(cls, d: TaskDict, /) -> Self:
        """Create task from dictionary representation."""
        task: Self = cls(**d)

        if task.resources:
            task.resources: set[AResource] = {(GLOBAL_RESOURCES[r] if isinstance(r, str) else r)
                                              for r in task.resources}

        task.status: TaskStatus = TaskStatus(task.status)

        return task

    @classmethod
    def from_str(cls, s: str, /) -> Self:
        """Create task from string representation."""
        return cls(ask=s)

    @classmethod
    def from_dict_or_str(cls, dict_or_str: TaskDict | str, /) -> Self:
        """Create task from dictionary or string representation."""
        if isinstance(dict_or_str, dict):
            return cls.from_dict(dict_or_str)

        if isinstance(dict_or_str, str):
            return cls.from_str(dict_or_str)

        raise TypeError(f'*** {dict_or_str} IS NEITHER A DICTIONARY NOR A STRING ***')

    def decompose(self) -> APlan:
        """Decompose task into modular plan."""
        assert isinstance(self.dynamic_decomposer, AbstractPlanner), '*** Dynamic Decomposer must be Planner instance ***'
        assert isinstance(self.dynamic_decomposer.max_depth), '*** Dynamic Decomposer must have positive Max Depth ***'

        for sub_plan in (plan := self.dynamic_decomposer.plan(problem=self.ask, resources=self.resources)):
            (sub_task := sub_plan.task).resources: set[AResource] = self.resources
            sub_task.dynamic_decomposer: APlanner = self.dynamic_decomposer.one_level_fewer_deep()

        return plan


ATask: TypeVar = TypeVar('ATask', bound=AbstractTask, covariant=False, contravariant=False)
