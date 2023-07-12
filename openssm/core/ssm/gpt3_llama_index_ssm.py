from base_ssm import BaseSSM
from openssm.core.slm.openai_slm import GPT3ChatCompletionSLM
# from openssm.core.adapter.llama_index_adapter import LlamaIndexAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class GPT3LlamaIndexSSM(BaseSSM):
    def __init__(self, backends: list[AbstractBackend]):
        slm = GPT3ChatCompletionSLM()
        adapter = None  # FIXME LlamaIndexAdapter()
        backends = None  # FIXME
        super().__init__(slm, adapter, backends)
