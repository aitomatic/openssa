"""Abstract agent with planning, reasoning & informational resources."""


from abc import ABC
from dataclasses import dataclass, field
from pprint import pprint

from openssa.l2.planning.abstract import APlan, APlanner
from openssa.l2.reasoning.abstract import AReasoner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.resource.abstract import AResource
from openssa.l2.task.task import Task


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

    def solve(self, problem: str, plan: APlan | None = None, dynamic: bool = True) -> str | None:
        """Solve problem, with an automatically generated plan (default) or explicitly specified plan."""
        if plan:
            if self.planner:
                if dynamic:
                    # if both Plan and Planner are given, and if solving dynamically,
                    # TODO: dynamic solution
                    raise NotImplementedError('Dynamic execution of given Plan and Planner not yet implemented')

                # if both Plan and Planner are given, and if solving statically,
                # then use Planner to update Plan's resources,
                # then execute such updated static Plan
                plan: APlan = self.planner.update_plan_resources(plan, resources=self.resources)
                pprint(plan)
                result: str = plan.execute(reasoner=self.reasoner)

            else:
                # if Plan is given but no Planner is, then execute Plan statically
                result: str = plan.execute(reasoner=self.reasoner)

        elif self.planner:
            if dynamic:
                # if no Plan is given but Planner is, and if solving dynamically,
                result: str = ...  # TODO: dynamic solution

            else:
                # if no Plan is given but Planner is, and if solving statically,
                # then use Planner to generate static Plan,
                # then execute such static plan
                plan: APlan = self.planner.plan(problem, resources=self.resources)
                pprint(plan)
                result: str = plan.execute(reasoner=self.reasoner)

        else:
            # if neither Plan nor Planner is given, directly use Reasoner
            result: str | None = self.reasoner.reason(task=Task(ask=problem, resources=self.resources))

        return result
