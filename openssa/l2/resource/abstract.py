"""Abstract Informational Resource."""


from abc import ABC, abstractmethod
from functools import cached_property
from typing import TypeVar

from ._prompts import RESOURCE_OVERVIEW_PROMPT_TEMPLATE


class AbstractResource(ABC):
    """Abstract Informational Resource."""

    @cached_property
    @abstractmethod
    def unique_name(self) -> str:
        """Return globally-unique name of Informational Resource."""

    @cached_property
    @abstractmethod
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of Informational Resource."""

    @cached_property
    def full_name(self):
        """Return full name for presenting Informational Resource clearly, especially in large prompts."""
        return f'INFORMATIONAL RESOURCE NAMED "{self.name}" (UNIQUELY NAMED "{self.unique_name}")'

    @abstractmethod
    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question from Informational Resource."""

    @cached_property
    def overview(self) -> str:
        """Return overview of Informational Resource."""
        return self.answer(question=RESOURCE_OVERVIEW_PROMPT_TEMPLATE.format(name=self.name))

    def present_full_answer(self, question: str, n_words: int = 1000) -> str:
        """Present answer to posed question together with full name & overview of Informational Resource."""
        return (f'{self.full_name}\n'
                'has the following overview:\n'
                f'```\n{self.overview}\n```\n'
                '\n'
                f'{self.full_name}\n'
                'returns the following answer/solution:\n'
                f'```\n{self.answer(question=question, n_words=n_words)}\n```\n')


AResource: TypeVar = TypeVar('AResource', bound=AbstractResource, covariant=False, contravariant=False)
