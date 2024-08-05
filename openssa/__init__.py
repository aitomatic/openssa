"""
======================================================
`OpenSSA`: SMALL SPECIALIST AGENTS FOR PROBLEM-SOLVING
======================================================

`OpenSSA` is an agentic AI framework for solving complex problems in real-world industry applications.
"""


from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import tomllib

from .core.agent.agent import Agent

from .core.program_space import ProgramSpace
from .core.programming.hierarchical.plan import HTP
from .core.programming.hierarchical.planner import HTPlanner

from .core.reasoning.base import BaseReasoner
from .core.reasoning.ooda import OodaReasoner

from .core.resource.file import FileResource

from .core.task import Task

from .core.util.lm.config import LMConfig
from .core.util.lm.huggingface import HuggingFaceLM
from .core.util.lm.llama import LlamaLM
from .core.util.lm.openai import OpenAILM


try:
    __version__: str = version(distribution_name='OpenSSA')

except PackageNotFoundError:
    with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
        __version__: str = tomllib.load(f)['tool']['poetry']['version']
