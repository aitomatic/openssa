"""Task Nature enum."""


from enum import StrEnum, auto


class TaskNature(StrEnum):
    """Task Nature enum."""

    RETRIEVE: str = auto()
    CALC: str = auto()
    ASSESS: str = auto()
