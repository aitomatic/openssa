from .base_ssm import BaseSSM
from core.slm.gpt3_slm import GPT3CompletionSLM, GPT3ChatCompletionSLM
from core.adapter.abstract_adapter import AbstractAdapter
from core.backend.abstract_backend import AbstractBackend


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
