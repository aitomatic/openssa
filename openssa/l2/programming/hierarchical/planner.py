"""
=========================
HIERARCHICAL TASK PLANNER
=========================

`HTPlanner` is `OpenSSA`'s default Programmer using LMs
to construct problem-solving Programs in the form of Hierarchical Task Plans (HTPs),
the complexity of which is controlled by 2 key parameters `max_depth` and `max_subtasks_per_decomp`.
"""


from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Self, TYPE_CHECKING

from openssa.l2.programming.abstract.programmer import AbstractProgrammer
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.task import Task

from .plan import HTP
from ._prompts import HTP_PROMPT_TEMPLATE, HTP_WITH_RESOURCES_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.util.lm.abstract import LMChatHist
    from .plan import HTPDict


@dataclass
class HTPlanner(AbstractProgrammer):
    """Hierarchical Task Planner."""

    # maximum allowed depth
    max_depth: int = 2

    # maximum number of sub-tasks per decomposition
    max_subtasks_per_decomp: int = 4

    def construct_htp(self, problem: str, *,
                      knowledge: set[Knowledge] | None = None,
                      resources: set[AResource] | None = None) -> HTP:
        """Construct HTP for solving posed Problem with given Knowledge and Informational Resources."""
        if self.max_depth > 0:
            prompt: str = (
                HTP_WITH_RESOURCES_PROMPT_TEMPLATE.format(problem=problem,
                                                          resource_overviews={resource.unique_name: resource.overview
                                                                              for resource in resources},
                                                          max_depth=1,
                                                          max_subtasks_per_decomp=self.max_subtasks_per_decomp)
                if resources
                else HTP_PROMPT_TEMPLATE.format(problem=problem,
                                                max_depth=1,
                                                max_subtasks_per_decomp=self.max_subtasks_per_decomp)
            )

            htp_dict: HTPDict = {}
            knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                    if knowledge
                                                    else None)
            while not (isinstance(htp_dict, dict) and htp_dict):
                htp_dict: HTPDict = self.lm.get_response(prompt, history=knowledge_lm_hist, json_format=True)

            htp: HTP = HTP.from_dict(htp_dict)

            htp.task.ask: str = problem
            htp.task.resources: set[AResource] | None = resources  # TODO: optimize to not always use all resources
            htp.programmer: Self = self

            sub_htp_programmer: Self = replace(self, max_depth=self.max_depth - 1)
            for sub_htp in htp.sub_htps:
                if resources:
                    sub_htp.task.resources: set[AResource] = resources  # TODO: optimize to not always use all resources
                sub_htp.programmer: Self = sub_htp_programmer

            return htp

        return HTP(task=Task(ask=problem, resources=resources))

    # alias
    construct_program = construct_htp
