from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.slm import GPT3ChatCompletionSLM
from openssm.core.ssm.rag_ssm import RAGSSM
from openssm.core.slm.abstract_slm import AbstractSLM


class SSM(RAGSSM):
    def __init__(self, slm: AbstractSLM = None, name: str = None):
        rag_backend = LlamaIndexBackend()
        super().__init__(slm=slm, rag_backend=rag_backend, name=name)


class GPT3SSM(SSM):
    def __init__(self, name: str = None):
        super().__init__(GPT3ChatCompletionSLM(), name=name)
