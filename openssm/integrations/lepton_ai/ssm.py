from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.integrations.lepton_ai.slm import ChatCompletionSLM


class ChatCompletionSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(ChatCompletionSLM(), adapter, backends)
