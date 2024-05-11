"""Base Reasoner."""


from dataclasses import dataclass
from typing import TYPE_CHECKING

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.task.abstract import ATask
from openssa.l2.task.status import TaskStatus

if TYPE_CHECKING:
    from openssa.l2.util.lm.abstract import LMChatHist

from ._prompts import RESOURCE_QA_CONSO_PROMPT_TEMPLATE


@dataclass
class BaseReasoner(AbstractReasoner):
    """Base Reasoner."""

    def reason(self, task: ATask, n_words: int = 1000, knowledge: set[str] = None) -> str:
        """Work through Task and return conclusion.

        Simply forward the question/problem to Task's available Information Resources,
        and then consolidate results from them.
        """
        messages: LMChatHist = []
        if knowledge is not None:
            messages.append({"role": "system", "content": "\n".join(s for s in knowledge)})
        task.result: str = ((self.lm.get_response(
                                prompt=RESOURCE_QA_CONSO_PROMPT_TEMPLATE.format(
                                    question=task.ask, n_words=n_words,
                                    resources_and_answers='\n\n'.join(r.present_full_answer(question=task.ask, n_words=n_words)  # noqa: E501
                                                                      for r in task.resources)), 
                                history=messages)

                             if len(task.resources) > 1

                             else next(iter(task.resources)).answer(question=task.ask, n_words=n_words))

                            if task.resources

                            else self.lm.get_response(prompt=f'`[WITHIN {n_words:,} WORDS:]`\n{task.ask}', history=messages))

        task.status: TaskStatus = TaskStatus.DONE

        return task.result
