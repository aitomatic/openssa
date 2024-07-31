from openssa.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssa.integrations.openai.ssm import GPT3ChatCompletionSLM
from openssa.core.ssm.rag_ssm import RAGSSM
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.integrations.lepton_ai.ssm import SLM as LeptonSLM
from openssa.core.slm.base_slm import PassthroughSLM


class SSM(RAGSSM):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        slm: AbstractSLM = None,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        rag_backend = LlamaIndexBackend(relevance_threshold=relevance_threshold)

        super().__init__(
            slm=slm, rag_backend=rag_backend, name=name, storage_dir=storage_dir
        )


class GPT3SSM(SSM):
    def __init__(
        self,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        super().__init__(
            slm=GPT3ChatCompletionSLM(),
            name=name,
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
        )


class GPT4SSM(SSM):
    def __init__(
        self,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        # pylint: disable=no-member

        super().__init__(
            slm=PassthroughSLM(),
            name=name,
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
        )


class LeptonLlamaIndexSSM(SSM):
    def __init__(
        self,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        super().__init__(
            name=name,
            slm=LeptonSLM(),
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
        )
