from llama_index.llms.base import LLM as RAGLLM
from llama_index.llms import OpenAI, AzureOpenAI
from openssa.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssa.integrations.openai.ssm import GPT3ChatCompletionSLM
from openssa.core.ssm.rag_ssm import RAGSSM
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.integrations.lepton_ai.ssm import SLM as LeptonSLM
from openssa.utils.config import Config
from openssa.core.slm.base_slm import PassthroughSLM


class SSM(RAGSSM):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        slm: AbstractSLM = None,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
        rag_llm: RAGLLM = None,
    ):
        rag_backend = LlamaIndexBackend(
            relevance_threshold=relevance_threshold, rag_llm=rag_llm
        )

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
        rag_llm = OpenAI(model="gpt-3.5-turbo-16k")

        super().__init__(
            slm=GPT3ChatCompletionSLM(),
            name=name,
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
            rag_llm=rag_llm,
        )


class GPT4SSM(SSM):
    def __init__(
        self,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        # pylint: disable=no-member
        rag_llm = AzureOpenAI(engine=Config.AZURE_GPT4_ENGINE)

        super().__init__(
            slm=PassthroughSLM(),
            name=name,
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
            rag_llm=rag_llm,
        )


class LeptonLlamaIndexSSM(SSM):
    def __init__(
        self,
        name: str = None,
        storage_dir: str = None,
        relevance_threshold: float = 0.5,
    ):
        rag_llm = OpenAI(model="gpt-3.5-turbo-16k")

        super().__init__(
            name=name,
            slm=LeptonSLM(),
            storage_dir=storage_dir,
            relevance_threshold=relevance_threshold,
            rag_llm=rag_llm,
        )
