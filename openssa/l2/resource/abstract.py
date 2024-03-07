"""Abstract informational resource."""


from abc import ABC, abstractmethod
from functools import cached_property

from ._prompts import RESOURCE_OVERVIEW_PROMPT_TEMPLATE


class AbstractResource(ABC):
    """Abstract informational resource."""

    @cached_property
    @abstractmethod
    def unique_name(self) -> str:
        """Return globally-unique name."""

    @cached_property
    @abstractmethod
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name."""

    @abstractmethod
    def answer(self, question: str) -> str:
        """Answer question from informational resource."""

    @cached_property
    def overview(self):
        """Return overview of informational resource."""
        return self.answer(question=RESOURCE_OVERVIEW_PROMPT_TEMPLATE.format(name=self.name))
