"""Abstract informational resource."""


from abc import ABC, abstractmethod
from functools import cached_property
from typing import TypeVar

from ._prompts import RESOURCE_OVERVIEW_PROMPT_TEMPLATE


class AbstractResource(ABC):
    """Abstract informational resource."""

    @cached_property
    @abstractmethod
    def unique_name(self) -> str:
        """Return globally-unique name of informational resource."""

    @cached_property
    @abstractmethod
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of informational resource."""

    @abstractmethod
    def answer(self, question: str, n_words: int = 300) -> str:
        """Answer question from informational resource."""

    @cached_property
    def overview(self) -> str:
        """Return overview of informational resource."""
        return self.answer(question=RESOURCE_OVERVIEW_PROMPT_TEMPLATE.format(name=self.name))


AResource: TypeVar = TypeVar('AResource', bound=AbstractResource, covariant=False, contravariant=False)
