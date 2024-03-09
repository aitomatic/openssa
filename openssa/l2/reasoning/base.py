"""Base reasoner."""


from dataclasses import dataclass

from openssa.l2.task.abstract import ATask

from .abstract import AbstractReasoner


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
class BaseReasoner(AbstractReasoner):
    """Base reasoner."""

    def reason(self, task: ATask) -> str:
        """Reason through task and return conclusion."""
        return (task.resource.answer(question=task.ask)
                if task.resource
                else self.lm.get_response(prompt=task.ask))
