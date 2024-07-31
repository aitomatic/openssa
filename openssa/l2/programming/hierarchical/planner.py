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
from typing import TYPE_CHECKING

from openssa.l2.programming.abstract.programmer import AbstractProgrammer
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.reasoning.ooda import OodaReasoner

from .plan import HTP
from ._prompts import HTP_PROMPT_TEMPLATE, HTP_WITH_RESOURCES_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.reasoning.abstract import AbstractReasoner
    from openssa.l2.resource.abstract import AbstractResource
    from openssa.l2.task import Task
    from openssa.l2.util.lm.abstract import LMChatHist
    from .plan import HTPDict


@dataclass
class HTPlanner(AbstractProgrammer):
    """Hierarchical Task Planner."""

    # maximum allowed depth
    max_depth: int = 2

    # maximum number of sub-tasks per decomposition
    max_subtasks_per_decomp: int = 4

    def construct_htp(self, task: Task, knowledge: set[Knowledge] | None = None, reasoner: AbstractReasoner | None = None) -> HTP:  # noqa: E501
        """Construct HTP for solving posed Problem with given Knowledge and Resources."""
        if not reasoner:
            reasoner: AbstractReasoner = OodaReasoner()

        if self.max_depth > 0:
            prompt: str = (
                HTP_WITH_RESOURCES_PROMPT_TEMPLATE.format(problem=task.ask,
                                                          resource_overviews={resource.unique_name: resource.overview
                                                                              for resource in task.resources},
                                                          max_depth=1,
                                                          max_subtasks_per_decomp=self.max_subtasks_per_decomp)
                if task.resources
                else HTP_PROMPT_TEMPLATE.format(problem=task.ask,
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

            htp.task: Task = task
            htp.task.resources: set[AbstractResource] | None = task.resources  # TODO: optimize to not always use all resources
            htp.programmer: HTPlanner = self
            htp.reasoner: AbstractReasoner = reasoner

            sub_htp_programmer: HTPlanner = replace(self, max_depth=self.max_depth - 1)
            for sub_htp in htp.sub_htps:
                if task.resources:
                    sub_htp.task.resources: set[AbstractResource] = task.resources  # TODO: optimize to not always use all resources
                sub_htp.programmer: HTPlanner = sub_htp_programmer
                sub_htp.reasoner: AbstractReasoner = reasoner

            return htp

        return HTP(task=task, programmer=self, reasoner=reasoner)

    # alias
    construct_program = construct_htp
