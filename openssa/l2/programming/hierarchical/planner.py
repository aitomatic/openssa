"""
=========================
HIERARCHICAL TASK PLANNER
=========================

`HTPlanner` is `OpenSSA`'s default Programmer using LMs
to construct problem-solving Programs in the form of Hierarchical Task Plans (HTPs),
the complexity of which is controlled by 2 key parameters `max_depth` and `max_subtasks_per_decomp`.
"""


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from openssa.l2.programming.abstract.programmer import AbstractProgrammer
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs

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

    # maximum number of sub-tasks per decomposition
    max_subtasks_per_decomp: int = 3

    def construct_htp(self, problem: str, *,
                      knowledge: set[Knowledge] | None = None,
                      resources: set[AResource] | None = None) -> HTP:
        """Construct HTP for solving posed Problem with given Knowledge and Informational Resources."""
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
        knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                if knowledge
                                                else None)
        while not (isinstance(htp_dict, dict) and htp_dict):
            htp_dict: HTPDict = self.lm.get_response(prompt, history=knowledge_lm_hist, json_format=True)

        htp: HTP = HTP.from_dict(htp_dict)

        if resources:
            htp.fix_missing_resources()

        return htp

    # alias
    construct_program = construct_htp
