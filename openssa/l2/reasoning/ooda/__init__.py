"""OODA Reasoner."""


from dataclasses import dataclass
from typing import TypedDict

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.task.abstract import ATask
from openssa.l2.task.status import TaskStatus

from ._prompts import ORIENT_PROMPT_TEMPLATE

from openssa.l2.util.lm.abstract import AbstractLM, LMChatMsg, LMChatHist

type Observation = str


class OrientResult(TypedDict):
    confident: bool
    answer: str


@dataclass
class OodaReasoner(AbstractReasoner):
    """OODA Reasoner."""

    def reason(self, task: ATask, n_words: int = 1000) -> str:
        """Work through Task and return conclusion.

        Use OODA loop to:
        - Observe results from available Informational Resources
        - Orient & Decide whether such results are adequate for confident answer/solution
        - Act to update Task's status and result
        """
        observations: set[Observation] = self.observe(task=task, n_words=n_words)

        # note: Orient & Decide steps are practically combined to economize LM calls
        orient_result: OrientResult = self.orient(task=task, observations=observations, n_words=n_words)
        decision: bool = self.decide(orient_result=orient_result)

        self.act(task=task, orient_result=orient_result, decision=decision)

        return task.result

    def observe(self, task: ATask, n_words: int = 1000) -> set[Observation]:
        """Observe results from available Informational Resources."""
        return {r.present_full_answer(question=task.ask, n_words=n_words) for r in task.resources}

    def orient(self, task: ATask, observations: set[Observation], n_words: int = 1000, knowledge: set[str] = None) -> OrientResult:
        """Orient whether observed results are adequate for directly resolving Task."""
        prompt: str = ORIENT_PROMPT_TEMPLATE.format(question=task.ask, n_words=n_words, observations='\n\n'.join(observations))  # noqa: E501

        def is_valid(orient_result_dict: OrientResult) -> bool:
            return (isinstance(orient_result_dict, dict) and
                    isinstance(orient_result_dict.get('confident'), bool) and
                    isinstance(orient_result_dict.get('answer'), str))

        orient_result_dict: OrientResult = {}
        while not is_valid(orient_result_dict):
            messages: LMChatHist = []
            if knowledge is not None:
                messages.append({"role": "system", "content": "\n".join(s for s in knowledge)})
            orient_result_dict: OrientResult = self.lm.get_response(prompt, history=messages, json_format=True)

        return orient_result_dict

    def decide(self, orient_result: OrientResult) -> bool:
        """Decide whether to directly resolve Task."""
        return orient_result['confident']

    def act(self, task: ATask, orient_result: OrientResult, decision: bool) -> str:
        """Update Task's status and result."""
        task.status: TaskStatus = TaskStatus.DONE if decision else TaskStatus.NEEDING_DECOMPOSITION
        task.result: str = orient_result['answer']
