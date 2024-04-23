"""Abstract agent with planning, reasoning & informational resources."""


from abc import ABC
from dataclasses import dataclass, field
from pprint import pprint
from typing import TYPE_CHECKING

from openssa.l2.planning.abstract.plan import APlan
from openssa.l2.planning.abstract.planner import APlanner
from openssa.l2.reasoning.abstract import AReasoner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.resource.abstract import AResource
from openssa.l2.task.status import TaskStatus
from openssa.l2.task.task import Task

if TYPE_CHECKING:
    from openssa.l2.task.abstract import ATask


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

    def solve(self, problem: str, plan: APlan | None = None, dynamic: bool = True) -> str:
        """Solve problem, with an automatically generated plan (default) or explicitly specified plan."""
        match (plan, self.planner, dynamic):
            case (None, None, _):
                # if neither Plan nor Planner is given, directly use Reasoner
                result: str = self.reasoner.reason(task=Task(ask=problem, resources=self.resources))

            case (None, _, False) if self.planner:
                # if no Plan is given but Planner is, and if solving statically,
                # then use Planner to generate static Plan,
                # then execute such static plan
                plan: APlan = self.planner.plan(problem, resources=self.resources)
                pprint(plan)
                result: str = plan.execute(reasoner=self.reasoner)

            case (None, _, True) if self.planner:
                # if no Plan is given but Planner is, and if solving dynamically,
                # then first directly use Reasoner,
                # and if that does not work, then use Planner to decompose 1 level more deeply,
                # and recurse until reaching confident solution or running out of depth
                result: str = self.solve_dynamically(problem=problem)

            case (_, None, _) if plan:
                # if Plan is given but no Planner is, then execute Plan statically
                result: str = plan.execute(reasoner=self.reasoner)

            case (_, _, False) if (plan and self.planner):
                # if both Plan and Planner are given, and if solving statically,
                # then use Planner to update Plan's resources,
                # then execute such updated static Plan
                plan: APlan = self.planner.update_plan_resources(plan, resources=self.resources)
                pprint(plan)
                result: str = plan.execute(reasoner=self.reasoner)

            case (_, _, True) if (plan and self.planner):
                # if both Plan and Planner are given, and if solving dynamically,
                # TODO: dynamic solution
                raise NotImplementedError('Dynamic execution of given Plan and Planner not yet implemented')

            case _:
                raise ValueError('*** Invalid Plan-Planner-Dynamism Combination ***')

        return result

    def solve_dynamically(self, problem: str) -> str:
        self.reasoner.reason(task := Task(ask=problem, resources=self.resources))

        if task.status == TaskStatus.NEEDING_DECOMPOSITION:
            task.dynamic_decomposer: APlanner = self.planner.one_level_deep()

            for sub_plan in (plan_1_level_deep := task.decompose()).sub_plans:
                sub_plan.task.dynamic_decomposer: APlanner = self.planner.one_fewer_level_deep()

            plan_1_level_deep.execute(reasoner=self.reasoner)

        return task.result
