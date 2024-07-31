"""Task Status enum."""


from enum import StrEnum, auto


class TaskStatus(StrEnum):
    """Task Status enum."""

    PENDING: str = auto()
    NEEDING_DECOMPOSITION: str = auto()
    DECOMPOSED: str = auto()
    DONE: str = auto()
