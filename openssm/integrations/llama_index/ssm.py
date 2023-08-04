from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.slm import GPT3ChatCompletionSLM


class BaseLlamaIndexSSM(BaseSSM):
    llama_backend: LlamaIndexBackend = None

    def __init__(self,
                 slm: AbstractSLM,
                 backends: list[AbstractBackend] = None,
                 name: str = None):
        adapter = BaseAdapter()
        backends = backends or []
        self.llama_backend = LlamaIndexBackend()
        backends.append(self.llama_backend)
        super().__init__(slm, adapter, backends, name)

    def get_llama_backend(self) -> LlamaIndexBackend:
        return self.llama_backend

    def read_directory(self, storage_dir: str = None, use_existing_index: bool = False):
        storage_dir = storage_dir or self._get_default_storage_dir()
        self.get_llama_backend().read_directory(storage_dir, use_existing_index)

    def read_gdrive(self, folder_id: str, storage_dir: str = None, use_existing_index: bool = False):
        storage_dir = storage_dir or self._get_default_storage_dir()
        self.get_llama_backend().read_gdrive(folder_id, storage_dir, use_existing_index)


class LlamaIndexSSM(BaseLlamaIndexSSM):
    def __init__(self, backends: list[AbstractBackend] = None, name: str = None):
        super().__init__(PassthroughSLM(), backends=backends, name=name)


class GPT3LlamaIndexSSM(BaseLlamaIndexSSM):
    def __init__(self, backends: list[AbstractBackend] = None, name: str = None):
        super().__init__(GPT3ChatCompletionSLM(), backends=backends, name=name)
