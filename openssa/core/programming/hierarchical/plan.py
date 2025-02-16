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

from dataclasses import dataclass, field, replace
from pprint import pformat
from types import SimpleNamespace
from typing import TypedDict, Required, NotRequired, TYPE_CHECKING

from loguru import logger
from openssa.core.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.core.programming.base.program import BaseProgram
from openssa.core.reasoning.ooda.ooda_reasoner import OodaReasoner
from openssa.core.task.status import TaskStatus
from openssa.core.task.task import Task, TaskDict
from tqdm import tqdm

from ._prompts import HTP_RESULTS_SYNTH_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.core.reasoning.base import BaseReasoner
    from openssa.core.resource.base import BaseResource
    from openssa.core.knowledge.base import Knowledge
    from openssa.core.util.misc import AskAnsPair

type HTPDict = TypedDict('HTPDict', {'task': Required[TaskDict | str],
                                     'sub-htps': NotRequired[list[HTPDict]]},
                         total=False)


class PLAN(SimpleNamespace):
    pass  # namespace class just for pretty-printing


@dataclass
class HTP(BaseProgram):
    """Hierarchical Task Plan (HTP)."""

    # decomposed sub-HTPs for solving target Task
    sub_htps: list[HTP] = field(default_factory=list,
                                init=True,
                                repr=True,
                                hash=None,
                                compare=True,
                                metadata=None,
                                kw_only=False)

    # Reasoner for working through individual Tasks to either conclude or make partial progress on them
    # (default: Observe-Orient-Decide-Act (OODA) Reasoner)
    reasoner: BaseReasoner = field(default_factory=OodaReasoner,
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
        return HTP(task=Task.from_dict_or_str(htp_dict['task']),
                   sub_htps=[HTP.from_dict(sub_htp_dict) for sub_htp_dict in htp_dict.get('sub-htps', [])])

    def to_dict(self) -> HTPDict:
        """Return dictionary representation."""
        return {'task': self.task.to_json_dict(),
                'sub-htps': [sub_htp.to_dict() for sub_htp in self.sub_htps]}

    def fill_missing_resources(self):
        """Fix missing Resources in HTP."""
        for sub_htp in self.sub_htps:
            if not sub_htp.task.resources:
                sub_htp.task.resources: set[BaseResource] = self.task.resources
            sub_htp.fill_missing_resources()

    def adapt(self, **kwargs: str):
        """Return adapted copy."""
        return replace(self,
                       task=replace(self.task, ask=self.task.ask.format(**kwargs)),
                       sub_htps=[sub_htp.adapt(**kwargs) for sub_htp in self.sub_htps])

    def execute(self, knowledge: set[Knowledge] | None = None, other_results: list[AskAnsPair] | None = None,
                allow_reject: bool = False) -> str:
        # pylint: disable=arguments-differ
        """Execute and return string result, using specified Reasoner to work through involved Task & Sub-Tasks.

        Execution also optionally takes into account domain-specific Knowledge and/or potentially elevant other results.
        """
        self.fill_missing_resources()  # TODO: optimize to not always use all resources

        # first, attempt direct solution with Reasoner
        reasoning_wo_sub_results: str = self.reasoner.reason(task=self.task, knowledge=knowledge,
                                                             other_results=other_results)  # noqa: E501

        if self.sub_htps:
            decomposed_htp: HTP = self

        # if Reasoner's result is unsatisfactory,
        # and if there is still allowed recursive depth,
        # use Programmer to decompose Problem into sub-HTPs
        elif (self.task.is_attempted and not self.task.is_done) and (self.programmer and self.programmer.max_depth):
            decomposed_htp: HTP = self.programmer.create_htp(task=self.task, knowledge=knowledge,
                                                             reasoner=self.reasoner)

        else:
            decomposed_htp = None

        # if there are sub-HTPs, recursively execute them and integrate their results
        if decomposed_htp:
            logger.info('\n'
                        'EXECUTING HIERACHICAL TASK PLAN (HTP)\n'
                        '=====================================\n'
                        f'\n{decomposed_htp.pformat}\n')

            sub_results: list[AskAnsPair] = []
            for sub_htp in tqdm(decomposed_htp.sub_htps):
                sub_results.append((sub_htp.task.ask, sub_htp.execute(knowledge=knowledge, other_results=sub_results)))

            # If the Reasoner allows for rejecting to answer due to lack of information
            if allow_reject:
                inputs: str = (
                        "If supporting information request for clarification or more information, "
                        "just request more information without doing any other thing. "
                        + '\n\n'.join((f'SUPPORTING QUESTION/TASK #{i + 1}:\n{ask}\n'
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
            else:
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

            self.task.result: str = self.reasoner.lm.get_response(
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

        # else, accept Reasoner's direct solution as final result
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
