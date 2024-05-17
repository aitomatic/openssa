"""OODA Reasoner."""


from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.task.status import TaskStatus
from openssa.l2.util.misc import format_other_result

from ._prompts import ORIENT_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.task.abstract import ATask
    from openssa.l2.util.lm.abstract import LMChatHist
    from openssa.l2.util.misc import AskAnsPair


type Observation = str


class OrientResult(TypedDict):
    confident: bool
    answer: str


@dataclass
class OodaReasoner(AbstractReasoner):
    """OODA Reasoner."""

    def reason(self, task: ATask, *,
               knowledge: set[Knowledge], other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> str:
        """Work through Task and return conclusion.

        Use OODA loop to:
        - Observe results from available Informational Resources
        - Orient & Decide whether such results are adequate for confident answer/solution
        - Act to update Task's status and result
        """
        observations: set[Observation] = self.observe(task=task, other_results=other_results, n_words=n_words)

        # note: Orient & Decide steps are practically combined to economize LM calls
        orient_result: OrientResult = self.orient(task=task, observations=observations,
                                                  knowledge=knowledge, n_words=n_words)
        decision: bool = self.decide(orient_result=orient_result)

        self.act(task=task, orient_result=orient_result, decision=decision)

        return task.result

    def observe(self, task: ATask, other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> set[Observation]:
        """Observe results from available Informational Resources."""
        observations: set[Observation] = {r.present_full_answer(question=task.ask, n_words=n_words)
                                          for r in task.resources}

        if other_results:
            observations |= {format_other_result(other_result) for other_result in other_results}

        return observations

    def orient(self, task: ATask, observations: set[Observation],
               knowledge: set[Knowledge] | None = None, n_words: int = 1000) -> OrientResult:
        """Orient whether observed results are adequate for directly resolving Task."""
        prompt: str = ORIENT_PROMPT_TEMPLATE.format(question=task.ask, n_words=n_words, observations='\n\n'.join(observations))  # noqa: E501

        def is_valid(orient_result_dict: OrientResult) -> bool:
            return (isinstance(orient_result_dict, dict) and
                    isinstance(orient_result_dict.get('confident'), bool) and
                    isinstance(orient_result_dict.get('answer'), str))

        orient_result_dict: OrientResult = {}
        knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                if knowledge
                                                else None)
        while not is_valid(orient_result_dict):
            orient_result_dict: OrientResult = self.lm.get_response(prompt, history=knowledge_lm_hist, json_format=True)

        return orient_result_dict

    def decide(self, orient_result: OrientResult) -> bool:
        """Decide whether to directly resolve Task."""
        return orient_result['confident']

    def act(self, task: ATask, orient_result: OrientResult, decision: bool) -> str:
        """Update Task's status and result."""
        task.status: TaskStatus = TaskStatus.DONE if decision else TaskStatus.NEEDING_DECOMPOSITION
        task.result: str = orient_result['answer']
