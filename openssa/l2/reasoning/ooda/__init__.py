"""OODA reasoner."""


from dataclasses import dataclass

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.task.abstract import ATask

from ._prompts import OBSERVE_PROMPT_TEMPLATE, ORIENT_PROMPT_TEMPLATE, DECIDE_PROMPT_TEMPLATE


@dataclass
class OodaReasoner(AbstractReasoner):
    """OODA reasoner."""

    def reason(self, task: ATask, n_words: int = 300) -> str:
        """Reason through task and return conclusion."""

        return result

    def observe(self, task: ATask) -> str:
        """Observe."""

    def orient(self, task: ATask) -> str:
        """Orient."""

    def decide(self, task: ATask) -> str:
        """Decide."""

    def act(self, task: ATask) -> str:
        """Act."""
