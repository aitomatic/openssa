from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.slm import GPT3ChatCompletionSLM
from openssm.core.ssm.rag_ssm import RAGSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.integrations.lepton_ai.slm import SLM as LeptonSLM

class SSM(RAGSSM):
    def __init__(self,
                 slm: AbstractSLM = None,
                 name: str = None,
                 storage_dir: str = None,
                 relevance_threshold: float = 0.5,
                 qa_template: str = None):
        rag_backend = LlamaIndexBackend(relevance_threshold=relevance_threshold)
        if qa_template is not None:
            rag_backend.query_engine_kwargs = {'text_qa_template': qa_template}

        super().__init__(slm=slm, rag_backend=rag_backend, name=name, storage_dir=storage_dir)


class GPT3SSM(SSM):
    def __init__(self,
                 name: str = None,
                 storage_dir: str = None,
                 relevance_threshold: float = 0.5):
        super().__init__(slm=GPT3ChatCompletionSLM(),
                         name=name,
                         storage_dir=storage_dir,
                         relevance_threshold=relevance_threshold)

class LeptonLlamaIndexSSM(SSM):
    def __init__(self,
                 name: str = None,
                 storage_dir: str = None,
                 relevance_threshold: float = 0.5):
        super().__init__(name=name,
                         slm=LeptonSLM(),
                         storage_dir=storage_dir,
                         relevance_threshold=relevance_threshold)
