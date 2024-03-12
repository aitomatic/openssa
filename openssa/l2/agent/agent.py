"""Agent with planning, reasoning & informational resources."""


from dataclasses import dataclass, field

from openssa.l2.planning.abstract import APlanner
from openssa.l2.planning.hierarchical import AutoHTPlanner

from .abstract import AbstractAgent


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
class Agent(AbstractAgent):
    """Agent with planning, reasoning & informational resources."""

    planner: APlanner = field(default_factory=AutoHTPlanner)
