import openai
from llama_index.llms.base import LLM as RAGLLM
from llama_index.llms import OpenAI, AzureOpenAI
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.ssm import GPT3ChatCompletionSLM
from openssm.core.ssm.rag_ssm import RAGSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.integrations.lepton_ai.ssm import SLM as LeptonSLM
from openssm.utils.config import Config
from openssm.core.slm.base_slm import PassthroughSLM


class SSM(RAGSSM):
    # pylint: disable=too-many-arguments
    def __init__(self,
                 slm: AbstractSLM = None,
                 name: str = None,
                 storage_dir: str = None,
                 relevance_threshold: float = 0.5,
                 rag_llm: RAGLLM = None):

        rag_backend = LlamaIndexBackend(relevance_threshold=relevance_threshold, rag_llm=rag_llm)

        super().__init__(slm=slm,
                         rag_backend=rag_backend,
                         name=name,
                         storage_dir=storage_dir)


class GPT3SSM(SSM):
    def __init__(self, name: str = None, storage_dir: str = None, relevance_threshold: float = 0.5):

        openai.api_base = Config.OPENAI_API_URL
        openai.api_key = Config.OPENAI_API_KEY
        print(f"Using OpenAI API: {openai.api_base}")
        print(f"Using OpenAI API Key: {openai.api_key}")
        rag_llm = OpenAI(model="gpt-3.5-turbo-16k")

        super().__init__(slm=GPT3ChatCompletionSLM(),
                         name=name,
                         storage_dir=storage_dir,
                         relevance_threshold=relevance_threshold,
                         rag_llm=rag_llm)

class GPT4SSM(SSM):
    def __init__(self, name: str = None, storage_dir: str = None, relevance_threshold: float = 0.5):

        # pylint: disable=no-member
        # TODO: think through how to get LlamaIndex to support both OpenAI and Azure simultaneously
        openai.api_base = Config.AZURE_GPT4_API_URL
        openai.api_key = Config.AZURE_GPT4_API_KEY
        openai.api_version = Config.AZURE_API_VERSION
        openai.api_type = 'azure'
        rag_llm = AzureOpenAI(engine=Config.AZURE_GPT4_ENGINE)

        super().__init__(slm=PassthroughSLM(),
                         name=name,
                         storage_dir=storage_dir,
                         relevance_threshold=relevance_threshold,
                         rag_llm=rag_llm)

class LeptonLlamaIndexSSM(SSM):
    def __init__(self, name: str = None, storage_dir: str = None, relevance_threshold: float = 0.5):

        openai.api_base = Config.OPENAI_API_URL
        openai.api_key = Config.OPENAI_API_KEY
        rag_llm = OpenAI(model="gpt-3.5-turbo-16k")

        super().__init__(name=name,
                         slm=LeptonSLM(),
                         storage_dir=storage_dir,
                         relevance_threshold=relevance_threshold,
                         rag_llm=rag_llm)
