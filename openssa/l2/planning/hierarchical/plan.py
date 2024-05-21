"""Hierarchical Task Plan (HTP)."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Self, TypedDict, Required, NotRequired, TYPE_CHECKING

from loguru import logger
from tqdm import tqdm

from openssa.l2.planning.abstract.plan import AbstractPlan
from openssa.l2.reasoning.base import BaseReasoner
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.task.abstract import TaskDict
from openssa.l2.task.status import TaskStatus
from openssa.l2.task.task import Task

from ._prompts import HTP_RESULTS_SYNTH_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.util.lm.abstract import LMChatHist
    from openssa.l2.util.misc import AskAnsPair


type HTPDict = TypedDict('HTPDict', {'task': Required[TaskDict | str],
                                     'sub-plans': NotRequired[list[Self]]},
                         total=False)


@dataclass
class HTP(AbstractPlan):
    """Hierarchical Task Plan (HTP)."""

    @classmethod
    def from_dict(cls, htp_dict: HTPDict, /) -> HTP:
        """Create HTP from dictionary representation."""
        return HTP(task=Task.from_dict_or_str(htp_dict['task']),  # pylint: disable=unexpected-keyword-arg
                   sub_plans=[HTP.from_dict(d) for d in htp_dict.get('sub-plans', [])])

    def to_dict(self) -> HTPDict:
        """Return dictionary representation."""
        return {'task': self.task.to_json_dict(),
                'sub-plans': [p.to_dict() for p in self.sub_plans]}

    def fix_missing_resources(self):
        """Fix missing Informational Resources in HTP."""
        for p in self.sub_plans:
            if not p.task.resources:
                p.task.resources: set[AResource] = self.task.resources
            p.fix_missing_resources()

    def execute(self, reasoner: AReasoner | None = None, knowledge: set[Knowledge] | None = None,
                other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account potentially-relevant other results from elsewhere.
        """
        if reasoner is None:
            reasoner: AReasoner = BaseReasoner()

        reasoning_wo_sub_results: str = reasoner.reason(task=self.task, knowledge=knowledge, other_results=other_results)

        if self.sub_plans:
            sub_results: list[AskAnsPair] = []
            for sub_plan in tqdm(self.sub_plans):
                sub_results.append((sub_plan.task.ask, (sub_plan.task.result
                                                        if sub_plan.task.status == TaskStatus.DONE
                                                        else sub_plan.execute(reasoner=reasoner, knowledge=knowledge,
                                                                              other_results=sub_results))))

            inputs: str = ('REASONING WITHOUT SUPPORTING/OTHER RESULTS '
                           '(preliminary conclusions here can be overriden by more convincing supporting/other data):\n'
                           f'{reasoning_wo_sub_results}\n'
                           '\n\n' +
                           '\n\n'.join((f'SUPPORTING QUESTION/TASK #{i + 1}:\n{ask}\n'
                                        '\n'
                                        f'SUPPORTING RESULT #{i + 1}:\n{result}\n')
                                       for i, (ask, result) in enumerate(sub_results)) +
                           (('\n\n' +
                             '\n\n'.join((f'OTHER QUESTION/TASK #{i + 1}:\n{ask}\n'
                                          '\n'
                                          f'OTHER RESULT #{i + 1}:\n{result}\n')
                                         for i, (ask, result) in enumerate(other_results)))
                            if other_results
                            else ''))

            self.task.result: str = reasoner.lm.get_response(
                prompt=HTP_RESULTS_SYNTH_PROMPT_TEMPLATE.format(ask=self.task.ask, info=inputs),
                history=knowledge_injection_lm_chat_msgs(knowledge=knowledge) if knowledge else None)

            logger.debug('\n'
                         'TASK-LEVEL REASONING with Supporting/Other Results\n'
                         '==================================================\n'
                         f'\n{self.pformat}\n'
                         f'\n{self.task.ask.upper()}\n'
                         '--------------------------\n'
                         f'{self.task.result}\n'
                         '\n'
                         ' ^ \n'
                         '/|\\\n'
                         ' | \n'
                         '\n'
                         f'{inputs}')

        else:
            self.task.result: str = reasoning_wo_sub_results

            logger.debug('\n'
                         'TASK-LEVEL REASONING\n'
                         '====================\n'
                         f'\n{self.task.ask.upper()}\n'
                         '--------------------------\n'
                         f'{self.task.result}\n')

        self.task.status: TaskStatus = TaskStatus.DONE
        return self.task.result
