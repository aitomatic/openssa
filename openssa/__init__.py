from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import tomllib

from openssa.core.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.core.ooda_rag.solver import OodaSSA
from openssa.core.prompts import Prompts
from openssa.core.slm.base_slm import BaseSLM
from openssa.core.ssa.ssa import BaseSSA
from openssa.core.ssm.base_ssm import BaseSSM
from openssa.integrations.azure.ssm import GPT3ChatCompletionSSM as AzureGPT3ChatCompletionSSM
from openssa.integrations.azure.ssm import GPT3CompletionSSM as AzureGPT3CompletionSSM
from openssa.integrations.azure.ssm import GPT4ChatCompletionSSM as AzureGPT4ChatCompletionSSM
from openssa.integrations.huggingface.ssm import Falcon7bSSM
from openssa.integrations.lepton_ai.ssm import SLM as LeptonSLM
from openssa.integrations.lepton_ai.ssm import SSM as LeptonSSM
from openssa.integrations.llama_index.ssm import GPT4SSM as GPT4LlamaIndexSSM
from openssa.integrations.llama_index.ssm import SSM as LlamaIndexSSM
from openssa.integrations.llama_index.ssm import LeptonLlamaIndexSSM
from openssa.integrations.openai.ssm import GPT3ChatCompletionSSM as OpenAIGPT3ChatCompletionSSM
from openssa.integrations.openai.ssm import GPT3CompletionSSM as OpenAIGPT3CompletionSSM
from openssa.utils.config import Config
from openssa.utils.logs import Logs, logger, mlogger
from openssa.utils.utils import Utils

from .l2.agent.agent import Agent

from .l2.planning.abstract import AbstractPlan, AbstractPlanner
from .l2.planning.hierarchical import HTP, AutoHTPlanner

from .l2.reasoning.abstract import AbstractReasoner
from .l2.reasoning.base import BaseReasoner
from .l2.reasoning.ooda import OodaReasoner

from .l2.resource.abstract import AbstractResource
from .l2.resource.file import FileResource

from .l2.task.abstract import AbstractTask
from .l2.task.task import Task


try:
    __version__: str = version(distribution_name='OpenSSA')

except PackageNotFoundError:
    with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
        __version__: str = tomllib.load(f)['tool']['poetry']['version']
