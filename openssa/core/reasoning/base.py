"""
==================
REASONER INTERFACE
==================

`BaseReasoner` is `OpenSSA`'s abstract base class for reasoning.

A reasoner has an LM and can `.reason(...)` through a given task (which can come with assigned informational resources),
optionally leveraging some given domain-specific knowledge and/or some other results from elsewhere,
and return a conclusion in string.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openssa.core.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.core.knowledge.base import Knowledge
    from openssa.core.task.task import Task
    from openssa.core.util.lm.base import BaseLM
    from openssa.core.util.misc import AskAnsPair


@dataclass
class BaseReasoner(ABC):
    """Reasoner abstract base class."""

    # language model for reasoning
    lm: BaseLM = field(default_factory=OpenAILM.from_defaults,
                       init=True,
                       repr=True,
                       hash=None,
                       compare=True,
                       metadata=None,
                       kw_only=False)

    @abstractmethod
    def reason(self, task: Task, *,
               knowledge: set[Knowledge], other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> str:
        """Work through Task and return conclusion in string."""
