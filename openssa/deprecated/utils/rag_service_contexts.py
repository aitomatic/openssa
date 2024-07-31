from __future__ import annotations
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import ServiceContext
from openssa.utils.config import Config


class ServiceContextManager:

    @classmethod
    def get_aitomatic_sc(cls, **kwargs) -> ServiceContext:
        temperature = Config.DEFAULT_TEMPERATURE
        model = kwargs.get("model", "aitomatic-llm")
        embed_model = kwargs.get("embed_model", "aitomatic-emb")
        return ServiceContext.from_defaults(
            llm=OpenAI(
                model=model,
                temperature=temperature,
                api_key=Config.AITOMATIC_API_KEY,
                api_base=Config.AITOMATIC_API_URL,
            ),
            embed_model=OpenAIEmbedding(
                model=embed_model,
                api_key=Config.AITOMATIC_API_KEY,
                api_base=Config.AITOMATIC_API_URL,
            ),
        )

    @classmethod
    def get_openai_sc(cls, **kwargs) -> ServiceContext:
        temperature = kwargs.get("temperature", Config.DEFAULT_TEMPERATURE)
        model = kwargs.get("model", "gpt-3.5-turbo")
        embed_model = kwargs.get("embed_model", "text-embedding-ada-002")
        if "temperature" in kwargs:
            del kwargs["temperature"]
        if "model" in kwargs:
            del kwargs["model"]
        if "embed_model" in kwargs:
            del kwargs["embed_model"]

        return ServiceContext.from_defaults(
            llm=OpenAI(model=model, temperature=temperature, **kwargs),
            embed_model=OpenAIEmbedding(model=embed_model, **kwargs),
        )

    @classmethod
    def get_azure_openai_sc(cls, **kwargs) -> ServiceContext:
        temperature = kwargs.get("temperature", Config.DEFAULT_TEMPERATURE)
        engine = kwargs.get("engine", "aiva-dev-gpt35")
        embed_model = kwargs.get("embed_model", "text-embedding-ada-002")
        deployment_name = kwargs.get("deployment_name", "text-embedding-ada-002")
        api_version = kwargs.get("api_version", Config.AZURE_API_VERSION)
        azure_endpoint = kwargs.get("azure_endpoint", Config.AZURE_OPENAI_API_URL)
        api_key = kwargs.get("api_key", Config.AZURE_OPENAI_API_KEY)

        return ServiceContext.from_defaults(
            llm=AzureOpenAI(
                temperature=temperature,
                engine=engine,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
                api_key=api_key,
            ),
            embed_model=AzureOpenAIEmbedding(
                model=embed_model,
                deployment_name=deployment_name,
                api_version=api_version,
                azure_endpoint=azure_endpoint,
                api_key=api_key,
            ),
        )

    @classmethod
    def get_openai_35_turbo_sc(cls, **kwargs) -> ServiceContext:
        return cls.get_openai_sc(model="gpt-3.5-turbo", **kwargs)

    @classmethod
    def get_azure_jp_openai_35_turbo_sc(cls) -> ServiceContext:
        return cls.get_azure_openai_sc()

    @classmethod
    def get_azure_openai_4_0125_preview_sc(cls) -> ServiceContext:
        return cls.get_azure_openai_sc(
            engine="gpt-4-0125",
            api_key=Config.US_AZURE_OPENAI_API_KEY,
            azure_endpoint=Config.US_AZURE_OPENAI_API_BASE,
        )

    @classmethod
    def get_openai_4_0125_preview_sc(cls) -> ServiceContext:
        return cls.get_openai_sc(model="gpt-4-0125-preview")
