from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.slm.openai_slm import GPT3ChatCompletionSLM
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.llama_index_backend import LlamaIndexBackend
from openssm.core.slm.abstract_slm import AbstractSLM


class BaseLlamaIndexSSM(BaseSSM):
    llama_backend: LlamaIndexBackend = None

    def __init__(self, slm: AbstractSLM, backends: list[AbstractBackend] = None):
        adapter = BaseAdapter()
        backends = backends or []
        self.llama_backend = LlamaIndexBackend()
        backends.append(self.llama_backend)
        super().__init__(slm, adapter, backends)

    def get_llama_backend(self) -> LlamaIndexBackend:
        return self.llama_backend

    def read_directory(self, directory_path: str):
        self.get_llama_backend().read_directory(directory_path)


class LlamaIndexSSM(BaseLlamaIndexSSM):
    def __init__(self, backends: list[AbstractBackend] = None):
        super().__init__(PassthroughSLM(), backends)


class GPT3LlamaIndexSSM(BaseSSM):
    def __init__(self, backends: list[AbstractBackend] = None):
        super().__init__(GPT3ChatCompletionSLM(), backends)
