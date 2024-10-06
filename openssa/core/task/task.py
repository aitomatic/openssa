"""
===================
TASK DATA STRUCTURE
===================

`OpenSSA`'s `Task` data structure keeps track of
what is asked, what informational resources are available, the nature, the status and the result of a task.
"""


from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import TYPE_CHECKING, TypedDict, Required, NotRequired

from openssa.core.resource._global import GLOBAL_RESOURCES

from .nature import TaskNature
from .status import TaskStatus

if TYPE_CHECKING:
    from openssa.core.resource.base import BaseResource


class TaskDict(TypedDict, total=False):
    ask: Required[str]
    resources: NotRequired[set[BaseResource]]
    nature: NotRequired[TaskNature]
    status: NotRequired[TaskStatus]
    result: NotRequired[str]


@dataclass
class Task:
    """Task."""

    ask: str
    resources: set[BaseResource] = field(default_factory=set)
    nature: TaskNature | None = None
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None

    @classmethod
    def from_dict(cls, d: TaskDict, /) -> Task:
        """Create Task from dictionary representation."""
        task: Task = cls(**d)

        if task.resources:
            task.resources: set[BaseResource] = {(GLOBAL_RESOURCES[resource] if isinstance(resource, str) else resource)  # noqa: E501
                                                 for resource in task.resources}

        if task.nature:
            task.nature: TaskNature = TaskNature(task.nature)

        task.status: TaskStatus = TaskStatus(task.status)

        return task

    def to_json_dict(self) -> dict:
        d: TaskDict = asdict(self)
        d['resources']: list[BaseResource] = list(d['resources'])
        return d

    @classmethod
    def from_str(cls, s: str, /) -> Task:
        """Create Task from string representation."""
        return cls(ask=s)

    @classmethod
    def from_dict_or_str(cls, dict_or_str: TaskDict | str, /) -> Task:
        """Create Task from dictionary or string representation."""
        if isinstance(dict_or_str, dict):
            return cls.from_dict(dict_or_str)

        if isinstance(dict_or_str, str):
            return cls.from_str(dict_or_str)

        raise TypeError(f'*** {dict_or_str} IS NEITHER A DICTIONARY NOR A STRING ***')

    def is_attempted(self) -> bool:
        """Check if Task has been attempted."""
        return self.status != TaskStatus.PENDING

    def is_done(self) -> bool:
        """Check if Task is done."""
        return self.status == TaskStatus.DONE
