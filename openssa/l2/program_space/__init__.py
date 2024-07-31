"""
=============================================================
PROGRAM SPACE for storing searchable problem-solving Programs
=============================================================
"""


from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, TYPE_CHECKING

from openssa.l2.knowledge._prompts import knowledge_injection_lm_chat_msgs
from openssa.l2.util.lm.openai import OpenAILM

from ._prompts import PROGRAM_SEARCH_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from openssa.l2.knowledge.abstract import Knowledge
    from openssa.l2.programming.abstract.program import AProgram
    from openssa.l2.resource.abstract import AResource
    from openssa.l2.task import Task
    from openssa.l2.util.lm.abstract import AnLM, LMChatHist


@dataclass
class ProgramSpace:
    """Program Space for storing searchable problem-solving Programs."""

    # informative descriptions of stored problem-solving Programs, indexed by name
    descriptions: dict[str, str] = field(default_factory=dict,
                                         init=True,
                                         repr=False,
                                         hash=None,
                                         compare=True,
                                         metadata=None,
                                         kw_only=False)

    # stored problem-solving Programs, indexed by name
    programs: dict[str, AProgram] = field(default_factory=dict,
                                          init=True,
                                          repr=False,
                                          hash=None,
                                          compare=True,
                                          metadata=None,
                                          kw_only=False)

    # language model for searching among stored problem-solving Programs
    lm: AnLM = field(default_factory=OpenAILM.from_defaults,
                     init=True,
                     repr=True,
                     hash=None,
                     compare=True,
                     metadata=None,
                     kw_only=False)

    def add_or_update_program(self, name: str, description: str, program: AProgram):
        """Add or update a Program with its unique identifying name & informative description."""
        self.descriptions[name]: str = description
        self.programs[name]: AProgram = program

    def find_program(self, task: Task, knowledge: set[Knowledge] | None = None,
                     adaptations_to_known_programs: dict[str, Any] | None = None) -> AProgram | None:
        """Find a suitable Program for the posed Problem, or return None."""
        knowledge_lm_hist: LMChatHist | None = (knowledge_injection_lm_chat_msgs(knowledge=knowledge)
                                                if knowledge
                                                else None)

        valid_responses: set[str] = set(self.descriptions)
        valid_responses.add('NONE')

        matching_program_name: str = ''
        while matching_program_name not in valid_responses:
            matching_program_name: str = self.lm.get_response(
                prompt=PROGRAM_SEARCH_PROMPT_TEMPLATE.format(problem=task.ask,
                                                             resource_overviews={resource.unique_name: resource.overview
                                                                                 for resource in task.resources},
                                                             program_descriptions=self.descriptions),
                history=knowledge_lm_hist)

        if matching_program_name == 'NONE':
            return None

        adapted_program: AProgram = self.programs[matching_program_name].adapt(**(adaptations_to_known_programs or {}))
        adapted_program.task: Task = task
        return adapted_program
