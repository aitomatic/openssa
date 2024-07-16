"""
===========================
ABSTRACT REASONER INTERFACE
===========================

`AbstractReasoner` is `OpenSSA`'s abstract base class for reasoning.

A reasoner has an LM and can `.reason(...)` through a given task (which can come with assigned informational resources),
optionally leveraging some given domain-specific knowledge and/or some other results from elsewhere,
and return a conclusion in string.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar, TYPE_CHECKING

# from openssa.l2.util.lm.openai import OpenAILM
from openssa.l2.util.lm.huggingface_lm import HuggingFaceLM

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task import Task
    from openssa.l2.util.lm.abstract import AnLM
    from openssa.l2.util.misc import AskAnsPair


@dataclass
class AbstractReasoner(ABC):
    """Abstract Reasoner."""

    # language model for reasoning
    # lm: AnLM = field(default_factory=OpenAILM.from_defaults,
    #                  init=True,
    #                  repr=True,
    #                  hash=None,
    #                  compare=True,
    #                  metadata=None,
    #                  kw_only=False)
    lm: AnLM = field(default_factory=HuggingFaceLM.from_defaults,
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


AReasoner: TypeVar = TypeVar('AReasoner', bound=AbstractReasoner, covariant=False, contravariant=False)
