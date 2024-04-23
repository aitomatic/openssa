"""Abstract task."""


from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, asdict, field
from typing import TYPE_CHECKING, Self, TypedDict, Required, NotRequired, TypeVar

from openssa.l2.resource._global import GLOBAL_RESOURCES

from .status import TaskStatus

if TYPE_CHECKING:
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

    def to_json_dict(self) -> dict:
        d: TaskDict = asdict(self)
        d['resources']: list[AResource] = list(d['resources'])
        return d

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


ATask: TypeVar = TypeVar('ATask', bound=AbstractTask, covariant=False, contravariant=False)
