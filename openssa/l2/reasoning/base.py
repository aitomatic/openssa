"""Base reasoner."""


from dataclasses import dataclass

from openssa.l2.task.abstract import ATask

from .abstract import AbstractReasoner


@dataclass
class BaseReasoner(AbstractReasoner):
    """Base reasoner."""

    def reason(self, task: ATask, n_words: int = 300) -> str:
        """Reason through task and return conclusion."""
        return (task.resource.answer(question=task.ask, n_words=n_words)
                if task.resource
                else self.lm.get_response(prompt=f'`[WITHIN {n_words:,} WORDS:]`\n{task.ask}'))
