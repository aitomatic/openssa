"""Abstract agent with planning, reasoning & informational resources."""


from abc import ABC
from dataclasses import dataclass, field
from pprint import pprint

from openssa.l2.planning.abstract.plan import APlan
from openssa.l2.planning.abstract.planner import APlanner
from openssa.l2.reasoning.abstract import AReasoner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.resource.abstract import AResource


@dataclass
class AbstractAgent(ABC):
    """Abstract agent with planning, reasoning & informational resources."""

    planner: APlanner | None = None
    reasoner: AReasoner = field(default_factory=BaseReasoner)
    resources: set[AResource] = field(default_factory=set,
                                      init=True,
                                      repr=True,
                                      hash=False,  # mutable
                                      compare=True,
                                      metadata=None,
                                      kw_only=True)

    @property
    def resource_overviews(self) -> dict[str, str]:
        return {r.unique_name: r.overview for r in self.resources}

    def solve(self, problem: str, plan: APlan | None = None) -> str:
        """Solve problem, with an automatically generated plan (default) or explicitly specified plan."""
        plan: APlan = (self.planner.update_plan_resources(plan, resources=self.resources)
                       if plan
                       else self.planner.plan(problem, resources=self.resources))
        pprint(plan)

        return plan.execute(reasoner=self.reasoner)
