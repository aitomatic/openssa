"""
=============================
ABSTRACT PROGRAMMER INTERFACE
=============================

`AbstractProgrammer` is `OpenSSA`'s abstract base class for using LMs to construct problem-solving Programs.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Self, TypeVar, TYPE_CHECKING

from openssa.l2.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.util.lm.abstract import AnLM
    from .program import AProgram


@dataclass
class AbstractProgrammer(ABC):
    """Abstract Programmer."""

    # language model for generating problem-solving Programs
    lm: AnLM = field(default_factory=OpenAILM.from_defaults,
                     init=True,
                     repr=True,
                     hash=None,
                     compare=True,
                     metadata=None,
                     kw_only=False)

    # maximum allowed depth
    max_depth: int = 2

    def _one_level_deep(self) -> Self:
        """Get a 1-level-deep Programmer with same other parameters."""
        return replace(self, max_depth=1)

    def _one_fewer_level_deep(self) -> Self:
        """Get a 1-fewer-level-deep Programmer with same other parameters."""
        return replace(self, max_depth=self.max_depth - 1)

    @abstractmethod
    def construct_program(self, problem: str, *,
                          knowledge: set[Knowledge] | None = None,
                          resources: set[AResource] | None = None) -> AProgram:
        """Construct a Program for solving the posed Problem using given Knowledge & Resources."""


AProgrammer: TypeVar = TypeVar('AProgrammer', bound=AbstractProgrammer, covariant=False, contravariant=False)
