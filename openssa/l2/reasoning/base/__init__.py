"""Base Reasoner."""


from dataclasses import dataclass

from openssa.l2.reasoning.abstract import AbstractReasoner
from openssa.l2.knowledge.abstract import Knowledge
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.task.abstract import ATask
from openssa.l2.task.status import TaskStatus

from ._prompts import RESOURCE_QA_CONSO_PROMPT_TEMPLATE


@dataclass
class BaseReasoner(AbstractReasoner):
    """Base Reasoner."""

    def reason(self, task: ATask, *, knowledge: set[Knowledge] | None = None, n_words: int = 1000) -> str:
        """Work through Task and return conclusion.

        Simply forward the question/problem to Task's available Information Resources,
        and then consolidate results from them.
        """
        task.result: str = ((self.lm.get_response(
                                prompt=RESOURCE_QA_CONSO_PROMPT_TEMPLATE.format(
                                    question=task.ask, n_words=n_words,
                                    resources_and_answers='\n\n'.join(r.present_full_answer(question=task.ask, n_words=n_words)  # noqa: E501
                                                                      for r in task.resources)),
                                history=(knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                         if knowledge
                                         else None))

                             if len(task.resources) > 1

                             else next(iter(task.resources)).answer(question=task.ask, n_words=n_words))

                            if task.resources

                            else self.lm.get_response(prompt=f'`[WITHIN {n_words:,} WORDS:]`\n{task.ask}',
                                                      history=(knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                               if knowledge
                                                               else None)))

        task.status: TaskStatus = TaskStatus.DONE

        return task.result
