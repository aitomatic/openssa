"""
======================================================
`OpenSSA`: SMALL SPECIALIST AGENTS FOR PROBLEM-SOLVING
======================================================

`OpenSSA` is an agentic AI framework for solving complex problems in real-world industry applications.
"""


from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import tomllib

from .core.agent.dana import DANA

from .core.program_store.program_store import ProgramStore
from .core.programming.hierarchical.plan import HTP
from .core.programming.hierarchical.planner import HTPlanner

from .core.reasoning.ooda.ooda_reasoner import OodaReasoner
from .core.reasoning.simple.simple_reasoner import SimpleReasoner

from .core.resource.file import FileResource

from .core.task.task import Task

from .core.util.lm.config import LMConfig
from .core.util.lm.huggingface import HuggingFaceLM
from .core.util.lm.llama import LlamaLM
from .core.util.lm.openai import OpenAILM


try:
    __version__: str = version(distribution_name='OpenSSA')

except PackageNotFoundError:
    with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
        __version__: str = tomllib.load(f)['tool']['poetry']['version']
