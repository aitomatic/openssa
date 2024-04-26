"""Agent with Planning, Reasoning & Informational Resources."""


from dataclasses import dataclass, field

from openssa.l2.planning.abstract.planner import APlanner
from openssa.l2.planning.hierarchical.planner import AutoHTPlanner
from openssa.l2.reasoning.abstract import AReasoner
from openssa.l2.reasoning.ooda import OodaReasoner

from .abstract import AbstractAgent


@dataclass
class Agent(AbstractAgent):
    """Agent with Planning, Reasoning & Informational Resources."""

    # use Automated Hierarchical Task Planner as default Planner
    planner: APlanner = field(default_factory=AutoHTPlanner)

    # use OODA as default Reasoner
    reasoner: AReasoner = field(default_factory=OodaReasoner)
