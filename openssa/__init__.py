from collections.abc import Sequence
from pathlib import Path
from sys import version_info
if version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

# pylint: disable=wrong-import-position
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


with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
    __version__: str = tomllib.load(f)['tool']['poetry']['version']


__all__: Sequence[str] = (
    '__version__',
)
