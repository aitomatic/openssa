"""Abstract Reasoner."""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar, TYPE_CHECKING

from openssa.l2.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task.abstract import ATask
    from openssa.l2.util.lm.abstract import AnLM
    from openssa.l2.planning.abstract.plan import AskAnsPair


@dataclass
class AbstractReasoner(ABC):
    """Abstract Reasoner."""

    # language model for reasoning
    lm: AnLM = field(default_factory=OpenAILM.from_defaults,
                     init=True,
                     repr=True,
                     hash=None,
                     compare=True,
                     metadata=None,
                     kw_only=False)

    @abstractmethod
    def reason(self, task: ATask, *, knowledge: set[Knowledge], other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> str:
        """Work through Task and return conclusion."""


AReasoner: TypeVar = TypeVar('AReasoner', bound=AbstractReasoner, covariant=False, contravariant=False)
