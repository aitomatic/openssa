from .base_ssm import BaseSSM
from ..slm.openai_slm import GPT3CompletionSLM
from ..slm.openai_slm import GPT3ChatCompletionSLM
from ..adapter.abstract_adapter import AbstractAdapter
from ..backend.abstract_backend import AbstractBackend


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
