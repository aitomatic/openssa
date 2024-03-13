"""Task Status enum."""


from enum import StrEnum, auto


class TaskStatus(StrEnum):
    PENDING: str = auto()
    IN_PROGRESS: str = auto()
    DONE: str = auto()
    FAILED: str = auto()
    TIMED_OUT: str = auto()
