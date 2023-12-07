import os

from dotenv import load_dotenv
from llama_index import ServiceContext
from llama_index.embeddings import AzureOpenAIEmbedding, OpenAIEmbedding
from llama_index.llms import AzureOpenAI, OpenAI
from llama_index.llms.base import LLM
from llama_index.llms.openai_utils import ALL_AVAILABLE_MODELS, CHAT_MODELS

# exetend ALL_AVAILABLE_MODELS to include the models we want to use
ALL_AVAILABLE_MODELS.update(
    {
        "01-ai/Yi-34B-Chat": 4096,
        "Intel/neural-chat-7b-v3-1": 4096,
        "llama2-70b": 4096,
        "llama2-13b": 4096,
        "llama2-7b": 4096,
    }
)

CHAT_MODELS.update(
    {
        "01-ai/Yi-34B-Chat": 4096,
        "Intel/neural-chat-7b-v3-1": 4096,
        "llama2-70b": 4096,
        "llama2-13b": 4096,
        "llama2-7b": 4096,
    }
)

# import logging, sys
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


load_dotenv(override=True)


class LlmBaseModel:
    llama2 = "llama2"
    azure_openai = "AzureOpenAI"
    openai = "OpenAI"
    yi = "yi"
    neural_chat = "neural chat"


class LlmModelSize:
    llama2_7b = "7B"
    neutral_chat_7b = "7b"
    yi_34 = "34"
    llama2_13b = "13B"
    llama2_70b = "70B"
    gpt4 = "GPT-4"
    gpt35 = "GPT-3.5"


class AitomaticBaseURL:
    llama2_70b = "https://llama2-70b.lepton.run/api/v1"
    llama2_7b = "https://llama2-7b.lepton.run/api/v1"
    intel_neural_chat_7b = "http://34.145.174.152:8000/v1"
    yi_34b = "http://35.230.174.89:8000/v1"


class LLMConfig:  # pylint: disable=too-many-public-methods
    @classmethod
    def get_service_context_llama_2_7b(cls) -> ServiceContext:
        llm = cls.get_llm_llama_2_7b()

        embed_model = OpenAIEmbedding(
            api_key=cls.get_llama_2_api_key(),
            api_base=AitomaticBaseURL.llama2_7b,
        )

        return ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

    @classmethod
    def get_service_context_llama_2_70b(cls) -> ServiceContext:
        llm = cls.get_llm_llama_2_70b()
        embed_model = cls.get_aito_embeddings()
        return ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

    @classmethod
    def get_llm(cls, base_model: str, model_size: str = "") -> LLM:
        # pylint: disable=too-many-return-statements
        if (base_model == LlmBaseModel.llama2) and (model_size == LlmModelSize.llama2_70b):
            return cls.get_llm_llama_2_70b()

        if (base_model == LlmBaseModel.llama2) and (model_size == LlmModelSize.llama2_7b):
            return cls.get_llm_llama_2_7b()

        if (base_model == LlmBaseModel.azure_openai) and (model_size == LlmModelSize.gpt35):
            return cls.get_llm_azure_jp_35_16k()

        if (base_model == LlmBaseModel.azure_openai) and (model_size == LlmModelSize.gpt4):
            return cls.get_llm_azure_jp_4_32k()

        if base_model == LlmBaseModel.openai and model_size == LlmModelSize.gpt4:
            return cls.get_llm_openai_4()

        if base_model == LlmBaseModel.yi:
            return cls.get_aitomatic_yi_34b()

        if base_model == LlmBaseModel.neural_chat:
            return cls.get_intel_neural_chat_7b()

        return cls.get_llm_openai_35_turbo()

    @classmethod
    def get_service_context_openai_35_turbo_1106(cls) -> ServiceContext:
        return ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo-1106", api_key=cls.get_openai_api_key()),
            embed_model=OpenAIEmbedding(api_key=cls.get_openai_api_key()),
        )

    @classmethod
    def get_service_context_openai_35_turbo(cls) -> ServiceContext:
        return ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo", api_key=cls.get_openai_api_key()),
            embed_model=OpenAIEmbedding(api_key=cls.get_openai_api_key()),
        )

    @classmethod
    def get_service_context_azure_jp_35(cls) -> ServiceContext:
        llm = AzureOpenAI(
            engine="aiva-dev-gpt35",
            model="gpt-35-turbo",
            temperature=0.0,
            api_version="2023-09-01-preview",
            api_key=cls.get_azure_jp_api_key(),
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

        embed_model = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name="text-embedding-ada-002",
            api_key=cls.get_azure_jp_api_key(),
            api_version="2023-09-01-preview",
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

        return ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

    @classmethod
    def get_service_context_azure_jp_35_16k(cls) -> ServiceContext:
        llm = cls.get_llm_azure_jp_35_16k()

        embed_model = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name="text-embedding-ada-002",
            api_key=cls.get_azure_jp_api_key(),
            api_version="2023-09-01-preview",
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

        return ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

    @classmethod
    def get_service_context_azure_gpt4(cls) -> ServiceContext:
        llm = AzureOpenAI(
            engine="gpt-4",
            model="gpt-4",
            temperature=0.0,
            api_version="2023-09-01-preview",
            api_key=cls.get_azure_jp_api_key(),
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

        embed_model = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name="text-embedding-ada-002",
            api_key=cls.get_azure_jp_api_key(),
            api_version="2023-09-01-preview",
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )
        return ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

    @classmethod
    def get_service_context_azure_gpt4_32k(cls) -> ServiceContext:
        llm = AzureOpenAI(
            engine="gpt-4-32k",
            model="gpt-4-32k",
            temperature=0.0,
            api_version="2023-09-01-preview",
            api_key=cls.get_azure_jp_api_key(),
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

        embed_model = AzureOpenAIEmbedding(
            model="text-embedding-ada-002",
            deployment_name="text-embedding-ada-002",
            api_key=cls.get_azure_jp_api_key(),
            api_version="2023-09-01-preview",
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )
        return ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
        )

    @classmethod
    def get_azure_jp_api_key(cls) -> str:
        assert (api_key := os.getenv("AZURE_OPENAI_API_KEY", "")), ValueError("AZURE_OPENAI_API_KEY is not set")
        return api_key

    @classmethod
    def get_openai_api_key(cls) -> str:
        assert (api_key := os.getenv("OPENAI_API_KEY", "")), ValueError("OPENAI_API_KEY is not set")
        return api_key

    @classmethod
    def get_llama_2_api_key(cls) -> str:
        assert (api_key := os.getenv("LEPTON_API_KEY", "twoun3dz0fzw289dgyp2rlb3kltti8zi")), \
            ValueError("LEPTON_API_KEY is not set")
        return api_key

    @classmethod
    def get_llm_openai_35_turbo_1106(cls) -> LLM:
        return OpenAI(model="gpt-3.5-turbo-1106", api_key=cls.get_openai_api_key())

    @classmethod
    def get_llm_openai_35_turbo_0613(cls) -> LLM:
        return OpenAI(model="gpt-3.5-turbo", api_key=cls.get_openai_api_key())

    @classmethod
    def get_llm_openai_35_turbo(cls) -> LLM:
        return OpenAI(model="gpt-3.5-turbo-0613", api_key=cls.get_openai_api_key())

    @classmethod
    def get_llm_openai_4(cls) -> LLM:
        return OpenAI(model="gpt-4", api_key=cls.get_openai_api_key())

    @classmethod
    def get_llm_azure_jp_35_16k(cls) -> LLM:
        return AzureOpenAI(
            engine="gpt-35-turbo-16k",
            model="gpt-35-turbo-16k",
            temperature=0.0,
            api_version="2023-09-01-preview",
            api_key=cls.get_azure_jp_api_key(),
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

    @classmethod
    def get_llm_azure_jp_4_32k(cls) -> LLM:
        return AzureOpenAI(
            engine="gpt-4-32k",
            model="gpt-4-32k",
            temperature=0.0,
            api_version="2023-09-01-preview",
            api_key=cls.get_azure_jp_api_key(),
            azure_endpoint="https://aiva-japan.openai.azure.com",
        )

    @classmethod
    def get_llm_llama_2_70b(cls) -> LLM:
        return OpenAI(
            model="llama2-70b",
            api_base=AitomaticBaseURL.llama2_70b,
            api_key=cls.get_llama_2_api_key(),
        )

    @classmethod
    def get_llm_llama_2_7b(cls) -> LLM:
        return OpenAI(
            model="llama2-7b",
            api_base=AitomaticBaseURL.llama2_7b,
            api_key=cls.get_llama_2_api_key(),
        )

    @classmethod
    def get_aitomatic_13b(cls) -> LLM:
        url_base = "http://35.199.34.91:8000/v1"  # not running
        llm = OpenAI(
            model="gpt-3.5-turbo-0613",
            api_base=url_base,
            additional_kwargs={"stop": "\n"},
        )
        return llm

    @classmethod
    def get_aitomatic_yi_34b(cls) -> LLM:  # running
        return OpenAI(
            model="01-ai/Yi-34B-Chat",
            api_base=AitomaticBaseURL.yi_34b,
            additional_kwargs={"stop": "\n###"},
        )

    @classmethod
    def get_intel_neural_chat_7b(cls) -> LLM:  # running
        return OpenAI(
            model="Intel/neural-chat-7b-v3-1",
            api_base=AitomaticBaseURL.intel_neural_chat_7b,
        )

    @classmethod
    def get_aito_embeddings(cls) -> OpenAIEmbedding:  # running
        url_base = "https://aimo-api-mvp.platform.aitomatic.com/api/v1"
        api_key = 'AITOMATIC'  # key to aitomatic
        embed_model = OpenAIEmbedding(
            api_base=url_base,
            api_key=api_key
        )
        return embed_model
