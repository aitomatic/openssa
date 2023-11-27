import os
from typing import Optional
from openssa.integrations.openai.ssm import SLM as OpenAISLM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.utils.config import Config
from openssa.core.ssm.base_ssm import BaseSSM
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.core.ssm.rag_ssm import RAGSSM as BaseRAGSSM, AbstractRAGBackend
from openssa.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssa.integrations.openai.ssm import APIContext as OpenAIAPIContext


Config.LEPTONAI_API_KEY: Optional[str] = os.environ.get('LEPTONAI_API_KEY') or None
Config.LEPTONAI_API_URL: Optional[str] = os.environ.get('LEPTONAI_API_URL') or None

# pylint: disable=too-many-instance-attributes
class APIContext(OpenAIAPIContext):
    @classmethod
    def from_defaults(cls):
        return APIContext.gpt3_defaults()

    @classmethod
    def gpt3_defaults(cls):
        api_context = OpenAIAPIContext.gpt3_defaults()
        api_context.key = Config.LEPTONAI_API_KEY
        api_context.base = Config.LEPTONAI_API_URL
        return api_context

    @classmethod
    def gpt4_defaults(cls):
        raise NotImplementedError("GPT-4 is not yet supported by Lepton.")


class SLM(OpenAISLM):
    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        if api_context is None:
            api_context = APIContext.from_defaults()

        super().__init__(api_context, adapter)


class SSM(BaseSSM):
    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None,
                 name: str = None):

        super().__init__(slm=SLM(), adapter=adapter, backends=backends, name=name)


class RAGSSM(BaseRAGSSM):
    def __init__(self,
                 rag_backend: AbstractRAGBackend = None,
                 name: str = None,
                 storage_dir: str = None):

        if rag_backend is None:
            rag_backend = LlamaIndexBackend()

        super().__init__(slm=SLM(), rag_backend=rag_backend, name=name, storage_dir=storage_dir)
