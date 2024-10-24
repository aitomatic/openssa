"""
=========================
HIERARCHICAL TASK PLANNER
=========================

`HTPlanner` is `OpenSSA`'s default Programmer using LMs
to create problem-solving Programs in the form of Hierarchical Task Plans (HTPs),
the complexity of which is controlled by 2 key parameters `max_depth` and `max_subtasks_per_decomp`.
"""


from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from openssa.core.programming.base.programmer import BaseProgrammer
from openssa.core.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.core.reasoning.ooda.ooda_reasoner import OodaReasoner
from openssa.core.task.task import Task

from .plan import HTP
from ._prompts import SIMPLIFIED_DECOMPOSITION_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.core.knowledge.base import Knowledge
    from openssa.core.reasoning.base import BaseReasoner
    from openssa.core.resource.base import BaseResource
    from openssa.core.util.lm.base import LMChatHist
    from .plan import HTPDict


SUBTASK_HEADER: str = '[SUB-QUESTION/PROBLEM/TASK]\n'


@dataclass
class HTPlanner(BaseProgrammer):
    """Hierarchical Task Planner."""

    # maximum allowed depth
    max_depth: int = 2

    # maximum number of sub-tasks per decomposition
    max_subtasks_per_decomp: int = 4

    def create_htp(self, task: Task, knowledge: set[Knowledge] | None = None, reasoner: BaseReasoner | None = None) -> HTP:  # noqa: E501
        """Construct HTP for solving posed Problem with given Knowledge and Resources."""
        if not reasoner:
            reasoner: BaseReasoner = OodaReasoner(lm=self.lm)

        if self.max_depth > 0:
            prompt: str = SIMPLIFIED_DECOMPOSITION_PROMPT_TEMPLATE.format(
                problem=task.ask,
                resource_overviews={resource.unique_name: resource.overview for resource in task.resources},
                max_subtasks_per_decomp=self.max_subtasks_per_decomp)

            knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                    if knowledge
                                                    else None)

            def split_if_valid(sub_task_descriptions_combined: list[str]) -> list[str] | None:
                return (sub_task_descriptions_combined.split(sep=SUBTASK_HEADER, maxsplit=-1)[1:]
                        if sub_task_descriptions_combined.startswith(SUBTASK_HEADER)
                        else None)

            sub_task_descriptions: list[str] = []
            while not sub_task_descriptions:
                sub_task_descriptions: list[str] = split_if_valid(
                    sub_task_descriptions_combined=self.lm.get_response(prompt=prompt, history=knowledge_lm_hist))

            sub_htplanner: HTPlanner = replace(self, max_depth=self.max_depth - 1)

            return HTP(task=task,
                       programmer=self,
                       sub_htps=[HTP(task=Task(ask=sub_task_description,
                                               resources=task.resources),  # TODO: optimize to not always use all
                                     programmer=sub_htplanner,
                                     reasoner=reasoner)
                                 for sub_task_description in sub_task_descriptions],
                       reasoner=reasoner)

        return HTP(task=task, programmer=self, reasoner=reasoner)

    # alias
    create_program = create_htp
