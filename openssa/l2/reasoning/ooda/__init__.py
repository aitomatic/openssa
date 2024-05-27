"""
=========================================
OBSERVE-ORIENT-DECIDE-ACT (OODA) REASONER
=========================================

`OodaReasoner` is `OpenSSA`'s default reasoning mechanism,
following John Boyd's well-known Observe-Orient-Decide-Act (OODA) loop paradigm (wikipedia.org/en/OODA_loop).

In the `Observe` step, the OODA reasoner gathers relevant available information from the task's resources,
as well as other results (if given).

In the `Orient` & `Decide` steps, practically combined for efficiency in this implementation,
the OODA reasoner evaluates whether a confident conclusion can be produced for the problem/question the task poses,
as well as what the best possible answer can be;
the OODA reasoner then decides to mark the task as either `DONE` or `NEEDING_DECOMPOSITION`.

In the `Act` step, the OODA reasoner updates the status of the task, per the previous step's decision.
"""


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
        """Work through Task and return conclusion in string.

        Use OODA loop to:

        - Observe results from available Informational Resources as well as other results (if given)
        - Orient & Decide whether such results are adequate for confident answer/conclusion/solution
        - Act to update Task's status and result
        """
        observations: set[Observation] = self._observe(task=task, other_results=other_results, n_words=n_words)

        # note: Orient & Decide steps are practically combined to economize LM calls
        orient_result: OrientResult = self._orient(task=task, observations=observations, knowledge=knowledge, n_words=n_words)  # noqa: E501
        decision: bool = self._decide(orient_result=orient_result)

        self._act(task=task, orient_result=orient_result, decision=decision)

        return task.result

    def _observe(self, task: ATask, other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> set[Observation]:  # noqa: E501
        """Observe results from available Informational Resources as well as other results (if given)."""
        observations: set[Observation] = {r.present_full_answer(question=task.ask, n_words=n_words) for r in task.resources}  # noqa: E501

        if other_results:
            observations |= {format_other_result(other_result) for other_result in other_results}

        return observations

    def _orient(self, task: ATask, observations: set[Observation],
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

    def _decide(self, orient_result: OrientResult) -> bool:
        """Decide whether to directly resolve Task."""
        return orient_result['confident']

    def _act(self, task: ATask, orient_result: OrientResult, decision: bool) -> str:
        """Update Task's status and result."""
        task.status: TaskStatus = TaskStatus.DONE if decision else TaskStatus.NEEDING_DECOMPOSITION
        task.result: str = orient_result['answer']
