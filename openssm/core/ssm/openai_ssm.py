from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.slm.openai_slm import GPT3CompletionSLM
from openssm.core.slm.openai_slm import GPT3ChatCompletionSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class GPT3CompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT3CompletionSLM(), adapter, backends)


class GPT3ChatCompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT3ChatCompletionSLM(), adapter, backends)
