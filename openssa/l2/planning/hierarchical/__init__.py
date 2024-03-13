"""Hierarchical task-planning classes."""


from __future__ import annotations

from dataclasses import dataclass, asdict, field
import json
from typing import TYPE_CHECKING, TypedDict, Required, NotRequired

from loguru import logger
from tqdm import tqdm

from openssa.l2.planning.abstract import AbstractPlan, AbstractPlanner
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.task.status import TaskStatus
from openssa.l2.task.task import Task

from ._prompts import (HTP_PROMPT_TEMPLATE, HTP_WITH_RESOURCES_PROMPT_TEMPLATE, HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE,
                       HTP_RESULTS_SYNTH_PROMPT_TEMPLATE)

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.task.abstract import TaskDict


class HTPDict(TypedDict, total=False):
    task: Required[TaskDict | str]
    sub_plans: NotRequired[list[HTPDict]]


type AskAnsPair = tuple[str, str]


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
        """Create HTP from dictionary representation."""
        return HTP(task=Task.from_dict_or_str(htp_dict['task']),  # pylint: disable=unexpected-keyword-arg
                   sub_plans=[HTP.from_dict(d) for d in htp_dict.get('sub-plans', [])])

    def to_dict(self) -> HTPDict:
        """Return dictionary representation of HTP."""
        return {'task': asdict(self.task),
                'sub-plans': [p.to_dict() for p in self.sub_plans]}

    def fix_missing_resources(self):
        """Fix missing resources in HTP."""
        for p in self.sub_plans:
            if not p.task.resource:
                p.task.resource: AResource | None = self.task.resource
            p.fix_missing_resources()

    def execute(self, reasoner: AReasoner = BaseReasoner(), other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified reasoner to reason through involved tasks."""
        reasoning_wo_sub_results: str = reasoner.reason(self.task)

        if self.sub_plans:
            sub_results: list[AskAnsPair] = []
            for p in tqdm(self.sub_plans):
                sub_result: AskAnsPair = p.task.ask, p.execute(reasoner, other_results=sub_results)
                sub_results.append(sub_result)

            prompt: str = HTP_RESULTS_SYNTH_PROMPT_TEMPLATE.format(
                ask=self.task.ask,
                info=(
                    f'REASONING WITHOUT FURTHER SUPPORTING RESULTS:\n{reasoning_wo_sub_results}\n'
                    '\n\n' +
                    '\n\n'.join((f'SUPPORTING QUESTION/TASK #{i + 1}:\n{ask}\n'
                                 '\n'
                                 f'SUPPORTING RESULT #{i + 1}:\n{result}\n')
                                for i, (ask, result) in enumerate(sub_results)) +
                    (('\n\n' +
                      '\n\n'.join((f'OTHER QUESTION/TASK #{i + 1}:\n{ask}\n'
                                   '\n'
                                   f'OTHER RESULT #{i + 1}:\n{result}\n')
                                  for i, (ask, result) in enumerate(other_results)))
                     if other_results
                     else '')
                )
            )
            logger.debug(prompt)

            self.task.result: str = reasoner.lm.get_response(prompt)

        else:
            self.task.result: str = reasoning_wo_sub_results

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
    max_subtasks_per_decomp: int = 3

    def plan(self, problem: str, resources: set[AResource] | None = None) -> HTP:
        """Make HTP for solving problem."""
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

    def update_plan_resources(self, plan: HTP, /, resources: set[AResource]) -> HTP:
        """Make updated HTP copy with relevant informational resources."""
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
