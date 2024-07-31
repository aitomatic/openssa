from openssa.deprecated.adapter.abstract_adapter import AbstractAdapter
from openssa.deprecated.backend.abstract_backend import AbstractBackend
from openssa.deprecated.ssm.base_ssm import BaseSSM

from openssa.deprecated.integrations.huggingface.slm import Falcon7bSLM


class Falcon7bSSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        super().__init__(Falcon7bSLM(), adapter, backends)
