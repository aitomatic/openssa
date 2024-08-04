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

from openssa.core.programming.abstract.programmer import AbstractProgrammer
from openssa.core.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.core.reasoning.ooda import OodaReasoner
from openssa.core.task import Task

from .plan import HTP
from ._prompts import SIMPLIFIED_DECOMPOSITION_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.core.knowledge.abstract import Knowledge
    from openssa.core.reasoning.abstract import AbstractReasoner
    from openssa.core.resource.abstract import AbstractResource
    from openssa.core.util.lm.abstract import LMChatHist
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
            reasoner: AbstractReasoner = OodaReasoner(lm=self.lm)

        if self.max_depth > 0:
            sub_task_descriptions: list[str] = self.lm.get_response(
                prompt=SIMPLIFIED_DECOMPOSITION_PROMPT_TEMPLATE.format(
                    problem=task.ask,
                    resource_overviews={resource.unique_name: resource.overview for resource in task.resources},
                    max_subtasks_per_decomp=self.max_subtasks_per_decomp),
                history=knowledge_injection_lm_chat_msgs(knowledge=knowledge) if knowledge else None,
                json_format=True)

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
    construct_program = construct_htp
