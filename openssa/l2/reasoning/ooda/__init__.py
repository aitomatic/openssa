"""OODA Reasoner."""


from dataclasses import dataclass
from typing import TypedDict

from loguru import logger

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.task.abstract import ATask
from openssa.l2.task.status import TaskStatus

from ._prompts import OBSERVE_PROMPT_TEMPLATE


type Observation = tuple[str, str, str]


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
        observations: list[Observation] = self.observe(task=task, n_words=n_words)

        # note: Orient & Decide steps are practically combined to economize LM calls
        orient_result: OrientResult = self.orient(task=task, observations=observations, n_words=n_words)
        decision: bool = self.decide(orient_result=orient_result)

        self.act(task=task, orient_result=orient_result, decision=decision)

        return task.result

    def observe(self, task: ATask, n_words: int = 1000) -> list[Observation]:
        """Observe results from available Informational Resources."""
        return [(r.name, r.overview, r.answer(question=task.ask, n_words=n_words))
                for r in task.resources]

    def orient(self, task: ATask, observations: list[Observation], n_words: int = 1000) -> OrientResult:
        """Orient whether observed results are adequate for directly resolving Task."""
        prompt: str = OBSERVE_PROMPT_TEMPLATE.format(
            question=task.ask, n_words=n_words,
            resources_and_answers='\n\n'.join((f'INFORMATIONAL RESOURCE #{i + 1} (name: "{name}"):\n'
                                               '\n'
                                               f'INFORMATIONAL RESOURCE #{i + 1} OVERVIEW:\n{overview}\n'
                                               '\n'
                                               f'ANSWER/SOLUTION #{i + 1}:\n{answer}\n')
                                              for i, (name, overview, answer) in enumerate(observations)))
        logger.debug(prompt)

        def is_valid(orient_result_dict: OrientResult) -> bool:
            return (isinstance(orient_result_dict.get('confident'), bool) and
                    isinstance(orient_result_dict.get('answer'), str))

        orient_result_dict: OrientResult = {}
        while not is_valid(orient_result_dict):
            orient_result_dict: OrientResult = self.lm.parse_output(self.lm.get_response(prompt))

        return orient_result_dict

    def decide(self, orient_result: OrientResult) -> bool:
        """Decide whether to directly resolve Task."""
        return orient_result['confident']

    def act(self, task: ATask, orient_result: OrientResult, decision: bool) -> str:
        """Update Task's status and result."""
        task.status: TaskStatus = TaskStatus.DONE if decision else TaskStatus.NEEDING_DECOMPOSITION
        task.result: str = orient_result['answer']
