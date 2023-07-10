from ..adapter.abstract_adapter import AbstractAdapter
from ..backend.abstract_backend import AbstractBackend
from ..slm.huggingface_slm import Falcon7bSLM
from ..slm.huggingface_slm import Falcon7bSLMLocal
from .base_ssm import BaseSSM


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
