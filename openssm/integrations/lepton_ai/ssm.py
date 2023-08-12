from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.integrations.lepton_ai.slm import SLM as LeptonSLM
from openssm.core.ssm.rag_ssm import RAGSSM as BaseRAGSSM, AbstractRAGBackend
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend


class SSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None,
                 name: str = None):

        super().__init__(slm=LeptonSLM(), adapter=adapter, backends=backends, name=name)


class RAGSSM(BaseRAGSSM):
    def __init__(self,
                 rag_backend: AbstractRAGBackend = None,
                 name: str = None,
                 storage_dir: str = None):

        if rag_backend is None:
            rag_backend = LlamaIndexBackend()

        super().__init__(slm=LeptonSLM(), rag_backend=rag_backend, name=name, storage_dir=storage_dir)
