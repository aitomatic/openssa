"""Abstract reasoner."""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from openssa.l2.task.abstract import ATask
from openssa.utils.llms import AnLLM, OpenAILLM


@dataclass
class AbstractReasoner(ABC):
    """Abstract reasoner."""

    lm: AnLLM = field(default_factory=OpenAILLM.get_gpt_4_1106_preview)

    # exit_condition: str = ...

    @abstractmethod
    def reason(self, task: ATask, n_words: int = 1000) -> str:
        """Reason through task and return conclusion."""


AReasoner: TypeVar = TypeVar('AReasoner', bound=AbstractReasoner, covariant=False, contravariant=False)
