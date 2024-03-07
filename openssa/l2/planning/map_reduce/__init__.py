"""Map-Reduce planning classes."""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openssa.l2.planning.abstract import AbstractPlan, AbstractPlanner
from openssa.l2.task.status import TaskStatus
from openssa.l2.task.task import Task
from openssa.utils.llms import AnLLM, OpenAILLM

if TYPE_CHECKING:
    from openssa.l2.resource.abstract import AbstractResource


class MRTP(AbstractPlan):
    """Map-Reduce task plan (MRTP)."""


class AutoMRTPlanner(AbstractPlanner):
    """Automated (generative) Map-Reduce task planner."""
