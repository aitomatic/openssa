"""Agent with planning, reasoning & informational resources."""


from dataclasses import dataclass, field

from openssa.l2.planning.abstract.planner import APlanner
from openssa.l2.planning.hierarchical import AutoHTPlanner

from .abstract import AbstractAgent


@dataclass
class Agent(AbstractAgent):
    """Agent with planning, reasoning & informational resources."""

    planner: APlanner = field(default_factory=AutoHTPlanner)
