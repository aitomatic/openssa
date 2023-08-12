from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.integrations.openai.slm import GPT3CompletionSLM, GPT3ChatCompletionSLM, GPT4ChatCompletionSLM


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


class GPT4ChatCompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(GPT4ChatCompletionSLM(), adapter, backends)
