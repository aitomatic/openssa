"""Automated (Generative) Hierarchical Task Planner."""


from __future__ import annotations

from dataclasses import dataclass
import json
from typing import TYPE_CHECKING

from openssa.l2.planning.abstract.planner import AbstractPlanner

from .plan import HTP, HTPDict
from ._prompts import HTP_PROMPT_TEMPLATE, HTP_WITH_RESOURCES_PROMPT_TEMPLATE, HTP_UPDATE_RESOURCES_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.resource.abstract import AResource


@dataclass
class AutoHTPlanner(AbstractPlanner):
    """Automated (Generative) Hierarchical Task Planner."""

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

        htp_dict: HTPDict = {}
        while not (isinstance(htp_dict, dict) and htp_dict):
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

        updated_htp_dict: HTPDict = {}
        while not (isinstance(updated_htp_dict, dict) and updated_htp_dict):
            updated_htp_dict: HTPDict = self.lm.parse_output(self.lm.get_response(prompt))

        updated_htp: HTP = HTP.from_dict(updated_htp_dict)

        updated_htp.fix_missing_resources()

        return updated_htp
