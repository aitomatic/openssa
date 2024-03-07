"""OODA reasoner."""


from dataclasses import dataclass

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.task.abstract import AbstractTask


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
class OodaReasoner(BaseReasoner):
    """OODA reasoner."""

    max_depth: int = 3

    # TODO: full OODA reasoning
