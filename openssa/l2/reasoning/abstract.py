"""Abstract reasoner."""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from openssa.l2.task.abstract import ATask
from openssa.utils.llms import AnLLM, OpenAILLM


@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=False,  # mutable
           match_args=True,
           kw_only=False,
           slots=False,
           weakref_slot=False)
class AbstractReasoner(ABC):
    """Abstract reasoner."""

    lm: AnLLM = field(default_factory=OpenAILLM.get_gpt_4_1106_preview)

    @abstractmethod
    def reason(self, task: ATask, n_words: int = 300) -> str:
        """Reason through task and return conclusion."""


AReasoner: TypeVar = TypeVar('AReasoner', bound=AbstractReasoner, covariant=False, contravariant=False)
