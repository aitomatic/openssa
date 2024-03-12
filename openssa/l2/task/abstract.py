"""Abstract task."""


from abc import ABC
from dataclasses import dataclass
from typing import Self, TypedDict, Required, NotRequired, TypeVar

from openssa.l2.resource.abstract import AbstractResource
from openssa.l2.resource._global import GLOBAL_RESOURCES

from .status import TaskStatus


class TaskDict(TypedDict, total=False):
    ask: Required[str]
    resource: NotRequired[AbstractResource]
    status: NotRequired[TaskStatus]
    result: NotRequired[str]


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
class AbstractTask(ABC):
    """Abstract task."""

    ask: str
    resource: AbstractResource | None = None
    status: TaskStatus = TaskStatus.PENDING
    result: str | None = None

    @classmethod
    def from_dict(cls, d: TaskDict, /) -> Self:
        """Create resource instance from dictionary representation."""
        task: Self = cls(**d)

        if isinstance(task.resource, str):
            task.resource: AbstractResource = GLOBAL_RESOURCES[task.resource]

        task.status: TaskStatus = TaskStatus(task.status)

        return task

    @classmethod
    def from_str(cls, s: str, /) -> Self:
        """Create resource instance from dictionary representation."""
        return cls(ask=s)

    @classmethod
    def from_dict_or_str(cls, dict_or_str: TaskDict | str, /) -> Self:
        """Create resource instance from dictionary or string representation."""
        if isinstance(dict_or_str, dict):
            return cls.from_dict(dict_or_str)

        if isinstance(dict_or_str, str):
            return cls.from_str(dict_or_str)

        raise TypeError(f'*** {dict_or_str} IS NEITHER A DICTIONARY NOR A STRING ***')


ATask: TypeVar = TypeVar('ATask', bound=AbstractTask, covariant=False, contravariant=False)
