from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.huggingface_slm import Falcon7bSLM
from openssm.core.slm.huggingface_slm import Falcon7bSLMLocal


class Falcon7bSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(Falcon7bSLM(), adapter, backends)


class Falcon7bSSMLocal(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(Falcon7bSLMLocal(), adapter, backends)
