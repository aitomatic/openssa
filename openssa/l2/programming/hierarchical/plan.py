"""
============================
HIERARCHICAL TASK PLAN (HTP)
============================

`HTP` is `OpenSSA`'s default problem-solving task plan structure.

A HTP instance is a tree, in which each node can be decomposed into a number of supporting sub-HTPs,
each targeting to solve a supporting sub-task.

HTP execution involves using a specified Reasoner
to work through sub-tasks from the lowest levels and roll up results up to the top level.

There is also a horizontal results-sharing mechanism
to enable the execution of a subsequent HTP node to benefit from results from earlier nodes at the same depth level.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pformat
from types import SimpleNamespace
from typing import Any, Self, TypedDict, Required, NotRequired, TYPE_CHECKING

from loguru import logger
from tqdm import tqdm

from openssa.l2.programming.abstract.program import AbstractProgram
from openssa.l2.reasoning.ooda import OodaReasoner
from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.task import TaskDict
from openssa.l2.task.status import TaskStatus
from openssa.l2.task import Task

from ._prompts import HTP_RESULTS_SYNTH_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.reasoning.abstract import AReasoner
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.util.lm.abstract import LMChatHist
    from openssa.l2.util.misc import AskAnsPair


type HTPDict = TypedDict('HTPDict', {'task': Required[TaskDict | str],
                                     'sub-htps': NotRequired[list[Self]]},
                         total=False)


class PLAN(SimpleNamespace):
    pass  # namespace class just for pretty-printing


@dataclass
class HTP(AbstractProgram):
    """Hierarchical Task Plan (HTP)."""

    # decomposed sub-HTPs for solving target Task
    sub_htps: list[Self] = field(default_factory=list,
                                 init=True,
                                 repr=True,
                                 hash=None,
                                 compare=True,
                                 metadata=None,
                                 kw_only=False)

    @property
    def quick_repr(self) -> PLAN:
        """Quick, pretty-formattable/printable namespace representation."""
        namespace: PLAN = PLAN(task=self.task.ask)

        if self.sub_htps:
            namespace.subs: list[PLAN] = [sub_htp.quick_repr for sub_htp in self.sub_htps]

        return namespace

    @property
    def pformat(self) -> str:
        """Pretty-formatted string representation."""
        return pformat(object=self.quick_repr,
                       indent=2,
                       width=120,
                       depth=None,
                       compact=False,
                       sort_dicts=False,
                       underscore_numbers=False).replace("'", '').replace('\\n', '')

    @classmethod
    def from_dict(cls, htp_dict: HTPDict, /) -> HTP:
        """Create HTP from dictionary representation."""
        return HTP(task=Task.from_dict_or_str(htp_dict['task']),  # pylint: disable=unexpected-keyword-arg
                   sub_htps=[HTP.from_dict(d) for d in htp_dict.get('sub-htps', [])])

    def to_dict(self) -> HTPDict:
        """Return dictionary representation."""
        return {'task': self.task.to_json_dict(),
                'sub-htps': [p.to_dict() for p in self.sub_htps]}

    def concretize_tasks_from_template(self, **kwargs: Any):
        self.task.ask: str = self.task.ask.format(**kwargs)

        for sub_htp in self.sub_htps:
            sub_htp.concretize_tasks_from_template(**kwargs)

    def fix_missing_resources(self):
        """Fix missing Resources in HTP."""
        for sub_htp in self.sub_htps:
            if not sub_htp.task.resources:
                sub_htp.task.resources: set[AResource] = self.task.resources
            sub_htp.fix_missing_resources()

    def execute(self, knowledge: set[Knowledge] | None = None,  # pylint: disable=arguments-differ
                reasoner: AReasoner | None = None,
                other_results: list[AskAnsPair] | None = None) -> str:
        """Execute and return string result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account domain-specific Knowledge and/or potentially elevant other results.
        """
        if reasoner is None:
            reasoner: AReasoner = OodaReasoner()

        reasoning_wo_sub_results: str = reasoner.reason(task=self.task, knowledge=knowledge, other_results=other_results)

        if self.sub_htps:
            sub_results: list[AskAnsPair] = []
            for sub_htp in tqdm(self.sub_htps):
                sub_results.append((sub_htp.task.ask, (sub_htp.task.result
                                                       if sub_htp.task.status == TaskStatus.DONE
                                                       else sub_htp.execute(knowledge=knowledge,
                                                                            reasoner=reasoner,
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
