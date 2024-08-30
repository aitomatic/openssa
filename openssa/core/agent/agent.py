"""
=====================
PROBLEM-SOLVING AGENT
=====================

This module contains `OpenSSA`'s main `Agent` class,
which brings together agentic problem-solving capabilities
leveraging domain-specific Knowledge and diverse Resources.

In solving a posed Problem, an Agent first
either finds from its Program Space a solution Program suitable for the posed Problem,
or constructs by its Programmer such a Program if there is no existing one.
The Agent then executes the found or constructed Program,
using an applicable execution engine/mechanism.

By default, `OpenSSA`'s Programs take the form of Hierarchical Task Plans (HTPs),
with their execution performed by an Observe-Orient-Decide-Act (OODA) reasoning mechanism.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from openssa.core.program_space import ProgramSpace
from openssa.core.programming.hierarchical.planner import HTPlanner
from openssa.core.task import Task

if TYPE_CHECKING:
    from openssa.core.programming.abstract.program import AbstractProgram
    from openssa.core.programming.abstract.programmer import AbstractProgrammer
    from openssa.core.knowledge.abstract import Knowledge
    from openssa.core.resource.abstract import AbstractResource


@dataclass
class Agent:
    """Problem-Solving Agent."""

    # Knowledge for use in Program search/construction and execution
    # (stored as a set of strings; default: empty set)
    knowledge: set[Knowledge] = field(default_factory=set,
                                      init=True,
                                      repr=False,
                                      hash=None,
                                      compare=True,
                                      metadata=None,
                                      kw_only=False)

    # Program Space for storing searchable problem-solving Programs
    # (default: empty collection)
    program_space: ProgramSpace = field(default_factory=ProgramSpace,
                                        init=True,
                                        repr=True,
                                        hash=None,
                                        compare=True,
                                        metadata=None,
                                        kw_only=False)

    # Programmer for constructing problem-solving Programs
    # (default: Hierarchical Task Planner)
    programmer: AbstractProgrammer = field(default_factory=HTPlanner,
                                           init=True,
                                           repr=True,
                                           hash=None,
                                           compare=True,
                                           metadata=None,
                                           kw_only=False)

    # Resources for answering information-querying questions
    # (default: empty set)
    resources: set[AbstractResource] = field(default_factory=set,
                                             init=True,
                                             repr=True,
                                             hash=None,
                                             compare=True,
                                             metadata=None,
                                             kw_only=False)

    def add_knowledge(self, *new_knowledge: Knowledge):
        """Add new Knowledge piece(s) stored in string(s)."""
        self.knowledge.update(new_knowledge)

    def add_resources(self, *new_resources: AbstractResource):
        """Add new Resource(s)."""
        self.resources.update(new_resources)

    def solve(self, problem: str, adaptations_from_known_programs: dict[str, Any] | None = None) -> str:
        """Solve the posed Problem.

        First either find from the Program Space a solution Program suitable for the Problem,
        or construct by the Programmer such a Program if there is no existing one.

        Then execute the found or constructed Program using an applicable execution engine/mechanism.
        """
        task: Task = Task(ask=problem, resources=self.resources)

        program: AbstractProgram = (
            self.program_space.find_program(task=task, knowledge=self.knowledge,
                                            adaptations_from_known_programs=adaptations_from_known_programs)
            or
            self.programmer.construct_program(task=task, knowledge=self.knowledge)
        )

        return program.execute(knowledge=self.knowledge)
