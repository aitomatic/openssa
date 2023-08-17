import os

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r', encoding='utf-8') as f:
    __version__ = f.read().strip()


from importlib.metadata import version

from openssm.core.prompts import Prompts
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.ssm.base_ssm import BaseSSM

from openssm.integrations.openai.ssm import (
    GPT3CompletionSSM as OpenAIGPT3CompletionSSM,
    GPT3ChatCompletionSSM as OpenAIGPT3ChatCompletionSSM
)

from openssm.integrations.azure.ssm import (
    GPT3CompletionSSM as AzureGPT3CompletionSSM,
    GPT3ChatCompletionSSM as AzureGPT3ChatCompletionSSM,
    GPT4ChatCompletionSSM as AzureGPT4ChatCompletionSSM
)

from openssm.integrations.huggingface.ssm import Falcon7bSSM

from openssm.integrations.llama_index.ssm import (
    SSM as LlamaIndexSSM,
    LeptonLlamaIndexSSM,
    GPT4SSM as GPT4LlamaIndexSSM
)

from openssm.integrations.lepton_ai.ssm import (
    SLM as LeptonSLM,
    SSM as LeptonSSM
)

from openssm.utils.config import Config
from openssm.utils.logs import Logs, logger, mlogger
from openssm.utils.utils import Utils
