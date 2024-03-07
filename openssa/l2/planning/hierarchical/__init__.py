"""Hierarchical task-planning classes."""


from __future__ import annotations

from dataclasses import dataclass, asdict, field
import json
from typing import TYPE_CHECKING

from loguru import logger
from tqdm import tqdm

from openssa.l2.planning.abstract import AbstractPlan, AbstractPlanner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.task.abstract import TaskDict
from openssa.l2.task.status import TaskStatus
from openssa.l2.task.task import Task
from openssa.utils.llms import AnLLM, OpenAILLM

from ._prompts import (HTP_PROMPT_TEMPLATE, HTP_WITH_RESOURCES_PROMPT_TEMPLATE, HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE,
                       HTP_RESULTS_SYNTH_PROMPT_TEMPLATE)

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AbstractReasoner
    from openssa.l2.resource.abstract import AbstractResource


HTPDict: type = dict[str, TaskDict | str | list[dict]]


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
class HTP(AbstractPlan):
    """Hierarchical task plan (HTP)."""

    sub_plans: list[HTP] = field(default_factory=list,
                                 init=True,
                                 repr=True,
                                 hash=False,  # mutable
                                 compare=True,
                                 metadata=None,
                                 kw_only=True)

    @classmethod
    def from_dict(cls, htp_dict: HTPDict, /) -> HTP:
        """Create hierarchical task plan from dictionary representation."""
        return HTP(task=Task.from_dict_or_str(htp_dict['task']),
                   sub_plans=[HTP.from_dict(d) for d in htp_dict.get('sub-plans', [])])

    def to_dict(self) -> HTPDict:
        """Return dictionary representation."""
        return {'task': asdict(self.task),
                'sub-plans': [p.to_dict() for p in self.sub_plans]}

    def fix_missing_resources(self):
        """Fix missing resources in HTP."""
        for p in self.sub_plans:
            if not p.task.resource:
                p.task.resource: AbstractResource | None = self.task.resource
            p.fix_missing_resources()

    def execute(self, reasoner: AbstractReasoner = BaseReasoner()) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""
        if self.sub_plans:
            sub_results: tuple[str, str] = ((p.task.ask, p.execute(reasoner)) for p in tqdm(self.sub_plans))

            prompt: str = HTP_RESULTS_SYNTH_PROMPT_TEMPLATE.format(
                ask=self.task.ask,
                supporting_info='\n\n'.join((f'SUPPORTING QUESTION/TASK #{i + 1}:\n{ask}\n'
                                             '\n'
                                             f'SUPPORTING RESULT #{i + 1}:\n{result}\n')
                                            for i, (ask, result) in enumerate(sub_results)))
            logger.debug(prompt)

            self.task.result: str = reasoner.lm.get_response(prompt)

        else:
            self.task.result: str = reasoner.reason(self.task)

        self.task.status: TaskStatus = TaskStatus.DONE
        return self.task.result


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
class AutoHTPlanner(AbstractPlanner):
    """Automated (generative) hierarchical task planner."""

    max_depth: int = 3
    max_subtasks_per_decomp: int = 9

    def plan(self, problem: str, resources: set[AbstractResource] | None = None) -> HTP:
        """Make hierarchical task plan (HTP) for solving problem."""
        prompt: str = (
            HTP_WITH_RESOURCES_PROMPT_TEMPLATE.format(problem=problem,
                                                      resource_overviews={r.unique_name: r.overview for r in resources},
                                                      max_depth=self.max_depth,
                                                      max_subtasks_per_decomp=self.max_subtasks_per_decomp)
            if resources
            else HTP_PROMPT_TEMPLATE.format(problem=problem,
                                            max_depth=self.max_depth,
                                            max_subtasks_per_decomp=self.max_subtasks_per_decomp)
        )

        # TODO: more rigorous JSON schema validation
        htp_dict: HTPDict = {}
        while not htp_dict:
            htp_dict: HTPDict = self.lm.parse_output(self.lm.get_response(prompt))

        htp: HTP = HTP.from_dict(htp_dict)

        if resources:
            htp.fix_missing_resources()

        return htp

    def update_plan_resources(self, plan: HTP, /, resources: set[AbstractResource]) -> HTP:
        """Make updated hierarchical task plan (HTP) copy with relevant informational resources."""
        assert isinstance(plan, HTP), TypeError(f'*** {plan} NOT OF TYPE {HTP.__name__} ***')
        assert resources, ValueError(f'*** {resources} NOT A NON-EMPTY SET OF INFORMATIONAL RESOURCES ***')

        prompt: str = HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE.format(resource_overviews={r.unique_name: r.overview
                                                                                      for r in resources},
                                                                  htp_json=json.dumps(obj=plan.to_dict()))

        # TODO: more rigorous JSON schema validation
        updated_htp_dict: HTPDict = {}
        while not updated_htp_dict:
            updated_htp_dict: HTPDict = self.lm.parse_output(self.lm.get_response(prompt))

        updated_htp: HTP = HTP.from_dict(updated_htp_dict)

        updated_htp.fix_missing_resources()

        return updated_htp
