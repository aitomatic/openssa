"""Agent with planning, reasoning & informational resources."""


from dataclasses import dataclass, field

from openssa.l2.planning.abstract import APlanner
from openssa.l2.planning.hierarchical import AutoHTPlanner
from openssa.l2.reasoning.abstract import AReasoner
from openssa.l2.reasoning.ooda import OodaReasoner

from .abstract import AbstractAgent


@dataclass
class Agent(AbstractAgent):
    """Agent with planning, reasoning & informational resources."""

    planner: APlanner = field(default_factory=AutoHTPlanner)
    reasoner: AReasoner = field(default_factory=OodaReasoner)
