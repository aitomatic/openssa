"""
===========================================================
DOMAIN-AWARE NEUROSYMBOLIC AGENT (DANA) FOR PROBLEM-SOLVING
===========================================================

This module contains `OpenSSA`'s `DANA` class,
which brings together agentic problem-solving capabilities
leveraging domain-specific Knowledge and diverse Resources.

In solving a posed Problem, a `DANA` agent first
either finds from its Program Store a solution Program suitable for the posed Problem,
or creates by its Programmer such a Program if there is no existing one.
The agent then executes the found or created Program,
using an applicable execution engine/mechanism.

By default, `OpenSSA`'s Programs take the form of Hierarchical Task Plans (HTPs),
with their execution performed by an Observe-Orient-Decide-Act (OODA) reasoning mechanism.
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from openssa.core.program_store.program_store import ProgramStore
from openssa.core.programming.hierarchical.planner import HTPlanner
from openssa.core.task.task import Task

if TYPE_CHECKING:
    from openssa.core.programming.base.program import BaseProgram
    from openssa.core.programming.base.programmer import BaseProgrammer
    from openssa.core.knowledge.base import Knowledge
    from openssa.core.resource.base import BaseResource


@dataclass
class DANA:
    """Domain-Aware Neurosymbolic Agent (`DANA`) for Problem-Solving."""

    # Knowledge for use in Program search/creation and execution
    # (stored as a set of strings; default: empty set)
    knowledge: set[Knowledge] = field(default_factory=set,
                                      init=True,
                                      repr=False,
                                      hash=None,
                                      compare=True,
                                      metadata=None,
                                      kw_only=False)

    # Program Store for storing searchable problem-solving Programs
    # (default: empty collection)
    program_store: ProgramStore = field(default_factory=ProgramStore,
                                        init=True,
                                        repr=True,
                                        hash=None,
                                        compare=True,
                                        metadata=None,
                                        kw_only=False)

    # Programmer for creating problem-solving Programs
    # (default: Hierarchical Task Planner)
    programmer: BaseProgrammer = field(default_factory=HTPlanner,
                                       init=True,
                                       repr=True,
                                       hash=None,
                                       compare=True,
                                       metadata=None,
                                       kw_only=False)

    # Resources for answering information-querying questions
    # (default: empty set)
    resources: set[BaseResource] = field(default_factory=set,
                                         init=True,
                                         repr=True,
                                         hash=None,
                                         compare=True,
                                         metadata=None,
                                         kw_only=False)

    def add_knowledge(self, *new_knowledge: Knowledge):
        """Add new Knowledge piece(s) stored in string(s)."""
        self.knowledge.update(new_knowledge)

    def add_resources(self, *new_resources: BaseResource):
        """Add new Resource(s)."""
        self.resources.update(new_resources)

    def solve(self, problem: str, adaptations_from_known_programs: dict[str, Any] | None = None,
              allow_reject: bool = False) -> str:
        """Solve the posed Problem.

        First either find from the Program Store a solution Program suitable for the Problem,
        or create by the Programmer such a Program if there is no existing one.

        Then execute the found or created Program using an applicable execution engine/mechanism.
        """
        task: Task = Task(ask=problem, resources=self.resources)

        program: BaseProgram = (
            self.program_store.find_program(task=task, knowledge=self.knowledge,
                                            adaptations_from_known_programs=adaptations_from_known_programs)
            or
            self.programmer.create_program(task=task, knowledge=self.knowledge)
        )

        return program.execute(knowledge=self.knowledge, allow_reject=allow_reject)
