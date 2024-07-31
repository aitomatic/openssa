from __future__ import annotations
from typing import Optional
import os
from llama_index.core import ServiceContext
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import OpenAI as LlamaIndexOpenAI
from llama_index.core.llms.llm import LLM  # noqa: TCH002
from llama_index.core.llms.openai_utils import ALL_AVAILABLE_MODELS, CHAT_MODELS
from openssa.utils.config import Config

# import sys
# import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Add the extended models to the list of available models in LlamaIndex
_EXTENDED_CHAT_MODELS = {
    "01-ai/Yi-34B-Chat": 4096,
    "Intel/neural-chat-7b-v3-1": 4096,
    "llama2-70b": 4096,
    "llama2-13b": 4096,
    "llama2-7b": 4096,
}
ALL_AVAILABLE_MODELS.update(_EXTENDED_CHAT_MODELS)
CHAT_MODELS.update(_EXTENDED_CHAT_MODELS)

# TODO: there should be a single Aitomatic api_base and api_key
Config.AITOMATIC_API_KEY: Optional[str] = os.environ.get("AITOMATIC_API_KEY")
Config.AITOMATIC_API_URL: Optional[str] = (
    os.environ.get("AITOMATIC_API_URL")
    or "https://aimo-api-mvp.platform.aitomatic.com/api/v1"
)
Config.AITOMATIC_API_URL_7B: Optional[str] = (
    os.environ.get("AITOMATIC_API_URL_7B") or "https://llama2-7b.lepton.run/api/v1"
)
Config.AITOMATIC_API_URL_70B: Optional[str] = (
    os.environ.get("AITOMATIC_API_URL_70B") or "https://llama2-70b.lepton.run/api/v1"
)

Config.OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
Config.OPENAI_API_URL: Optional[str] = (
    os.environ.get("OPENAI_API_URL") or "https://api.openai.com/v1"
)

Config.AZURE_OPENAI_API_KEY: Optional[str] = os.environ.get("AZURE_OPENAI_API_KEY")
Config.AZURE_OPENAI_API_URL: Optional[str] = (
    os.environ.get("AZURE_OPENAI_API_URL") or "https://aiva-japan.openai.azure.com"
)

Config.LEPTON_API_KEY: Optional[str] = os.environ.get("LEPTON_API_KEY")
Config.LEPTON_API_URL: Optional[str] = (
    os.environ.get("LEPTON_API_URL") or "https://llama2-7b.lepton.run/api/v1"
)


class LlamaIndexApi:  # no-pylint: disable=too-many-public-methods

    class LLMs:
        """
        This class represents the LLMs from different services
        """

        class _AnOpenAIAPIProvider:
            """
            This class represents an OpenAI-API provider
            """

            @classmethod
            def _get(cls, model=None, api_base=None, api_key=None, additional_kwargs=None) -> LLM:
                if model is None:
                    if api_base is None:
                        llm = LlamaIndexOpenAI(api_key=api_key, additional_kwargs=additional_kwargs)
                    else:
                        llm = LlamaIndexOpenAI(api_key=api_key, additional_kwargs=additional_kwargs)
                elif api_base is None:
                    llm = LlamaIndexOpenAI(api_key=api_key, additional_kwargs=additional_kwargs)
                else:
                    llm = LlamaIndexOpenAI(model=model, api_base=api_base, api_key=api_key)

                # Forcibly set the get_openai method to the _get_client method
                llm.__dict__['get_openai'] = llm._get_client  # pylint: disable=protected-access

                return llm

        class Aitomatic(_AnOpenAIAPIProvider):
            """
            This class represents the Aitomatic-hosted LLMs
            """

            @classmethod
            def get(cls, model=None, api_base=None, api_key=None, additional_kwargs=None) -> LLM:
                if model is None:
                    model = "llama2-7b"
                if api_key is None:
                    api_key = Config.AITOMATIC_API_KEY
                return super()._get(model=model, api_base=api_base, api_key=api_key, additional_kwargs=additional_kwargs)

            @classmethod
            def get_llama2_70b(cls) -> LLM:
                # TODO: there should be a single Aitomatic api_base and api_key
                llm = cls.get(
                    model="llama2-70b",
                    api_base=Config.AITOMATIC_API_URL_70B,
                    api_key=Config.LEPTON_API_KEY,
                )
                return llm

            @classmethod
            def get_llama2_7b(cls) -> LLM:
                # TODO: there should be a single Aitomatic api_base and api_key
                llm = cls.get(
                    model="llama2-7b",
                    api_base=Config.AITOMATIC_API_URL,
                    api_key=Config.LEPTON_API_KEY,
                )
                return llm

            @classmethod
            def get_13b(cls) -> LLM:
                # TODO: there should be a single Aitomatic api_base and api_key
                # not running
                llm = cls.get(
                    model="gpt-3.5-turbo-0613",
                    api_base="http://35.199.34.91:8000/v1",
                    additional_kwargs={"stop": "\n"},
                )
                return llm

            @classmethod
            def get_yi_34b(cls) -> LLM:  # running
                llm = cls.get(
                    model="01-ai/Yi-34B-Chat",
                    api_base="http://35.230.174.89:8000/v1",
                    additional_kwargs={"stop": "\n###"},
                )
                return llm

            @classmethod
            def get_intel_neural_chat_7b(cls) -> LLM:  # running
                llm = cls.get(
                    model="Intel/neural-chat-7b-v3-1",
                    api_base="http://34.145.174.152:8000/v1",
                )
                return llm

            @classmethod
            def get_aimo(cls):
                llm = cls.get(api_base=os.environ.get("AIMO_STANDARD_URL_BASE"))
                return llm

        class OpenAI(_AnOpenAIAPIProvider):
            """
            This class represents the OpenAI-hosted LLMs
            """

            @classmethod
            def get(cls, model=None) -> LLM:
                if model is None:
                    model = "gpt-3.5-turbo-1106"
                return super()._get(model=model, api_key=Config.OPENAI_API_KEY)

            @classmethod
            def get_gpt_35_turbo_1106(cls) -> LLM:
                return cls.get(model="gpt-3.5-turbo-1106")

            @classmethod
            def get_gpt_35_turbo_0613(cls) -> LLM:
                return cls.get(model="gpt-3.5-turbo")

            @classmethod
            def get_gpt_35_turbo(cls) -> LLM:
                return cls.get(model="gpt-3.5-turbo-0613")

            @classmethod
            def get_gpt_4(cls) -> LLM:
                return cls.get(model="gpt-4")

        class Azure:
            """
            This class represents the Azure-hosted LLMs
            """

            @classmethod
            def _get(cls, model=None, engine=None, api_base=None) -> LLM:
                if model is None:
                    model = "gpt-35-turbo-16k"
                if engine is None:
                    engine = "aiva-dev-gpt35"
                if api_base is None:
                    api_base = Config.AZURE_OPENAI_API_URL

                return AzureOpenAI(
                    engine=model,
                    model=model,
                    temperature=0.0,
                    api_version="2023-09-01-preview",
                    api_key=Config.AZURE_OPENAI_API_KEY,
                    azure_endpoint=api_base,
                )

            @classmethod
            def get(cls) -> LLM:
                return cls.get_gpt_35()

            @classmethod
            def get_gpt_35(cls) -> LLM:
                return cls._get(model="gpt-35-turbo")

            @classmethod
            def get_gpt_35_16k(cls) -> LLM:
                return cls._get(model="gpt-35-turbo-16k")

            @classmethod
            def get_gpt_4(cls) -> LLM:
                return cls.get_gpt_4_32k()

            @classmethod
            def get_gpt_4_32k(cls) -> LLM:
                return cls._get(model="gpt-4-32k")

    class Embeddings:
        """
        This class represents the different embedding services
        """

        class Aitomatic:
            """
            This class represents the Aitomatic-hosted embedding service
            """

            @classmethod
            def _get(cls, api_base=None, api_key=None) -> OpenAIEmbedding:
                if api_key is None:
                    api_key = Config.AITOMATIC_API_KEY
                return OpenAIEmbedding(api_base=api_base, api_key=api_key)

            @classmethod
            def get(cls) -> OpenAIEmbedding:  # running
                return cls._get(api_base=Config.AITOMATIC_API_URL)

            @classmethod
            def get_llama2_7b(cls) -> OpenAIEmbedding:
                return cls._get(api_base=Config.AITOMATIC_API_URL_7B)

            @classmethod
            def get_llama2_70b(cls) -> OpenAIEmbedding:
                return cls._get(api_base=Config.AITOMATIC_API_URL_70B)

        class OpenAI:
            """
            This class represents the OpenAI-hosted embedding service
            """

            @classmethod
            def get(cls) -> OpenAIEmbedding:
                return OpenAIEmbedding(api_key=Config.OPENAI_API_KEY)

        class Azure:
            """
            This class represents the Azure-hosted embedding service
            """

            @classmethod
            def get(cls) -> AzureOpenAIEmbedding:
                return AzureOpenAIEmbedding(
                    model="text-embedding-ada-002",
                    deployment_name="text-embedding-ada-002",
                    api_key=Config.AZURE_OPENAI_API_KEY,
                    api_version="2023-09-01-preview",
                    azure_endpoint=Config.AZURE_OPENAI_API_URL,
                )

    class ServiceContexts:
        """
        This class represents the service contexts for different models.
        """

        class _AServiceContextHelper:
            """
            This class represents the service contexts for the different embedding services.
            """

            @classmethod
            def _get(cls, llm=None, embedding=None) -> ServiceContext:
                sc = ServiceContext.from_defaults(llm=llm, embed_model=embedding)
                return sc

        class Aitomatic(_AServiceContextHelper):
            """
            This class represents the service contexts for the Aitomatic-hosted models.
            """

            @classmethod
            def get_llama2_7b(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Aitomatic.get_llama2_7b()
                embedding = LlamaIndexApi.Embeddings.Aitomatic.get_llama2_7b()
                return cls._get(llm=llm, embedding=embedding)

            @classmethod
            def get_llama_2_70b(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Aitomatic.get_llama2_7b()
                embedding = LlamaIndexApi.Embeddings.Aitomatic.get_llama2_70b()
                return cls._get(llm=llm, embedding=embedding)

        class OpenAI(_AServiceContextHelper):
            """
            This class represents the service contexts for the OpenAI-hosted models.
            """

            @classmethod
            def get_gpt_35_turbo_1106(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.OpenAI.get_gpt_35_turbo_1106()
                embedding = LlamaIndexApi.Embeddings.OpenAI.get()
                return cls._get(llm=llm, embedding=embedding)

            @classmethod
            def get_gpt_35_turbo(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.OpenAI.get_gpt_35_turbo()
                embedding = LlamaIndexApi.Embeddings.OpenAI.get()
                return cls._get(llm=llm, embedding=embedding)

        class Azure(_AServiceContextHelper):
            """
            This class represents the service contexts for the Azure-hosted models.
            """

            @classmethod
            def get(cls) -> ServiceContext:
                return cls.get_gpt_35()

            @classmethod
            def get_gpt_35(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Azure.get_gpt_35()
                embedding = LlamaIndexApi.Embeddings.Azure.get()
                return cls._get(llm=llm, embedding=embedding)

            @classmethod
            def get_gpt_35_16k(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Azure.get_gpt_35_16k()
                embedding = LlamaIndexApi.Embeddings.Azure.get()
                return cls._get(llm=llm, embedding=embedding)

            @classmethod
            def get_gpt4(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Azure.get_gpt_4()
                embedding = LlamaIndexApi.Embeddings.Azure.get()
                return cls._get(llm=llm, embedding=embedding)

            @classmethod
            def get_gpt4_32k(cls) -> ServiceContext:
                llm = LlamaIndexApi.LLMs.Azure.get_gpt_4_32k()
                embedding = LlamaIndexApi.Embeddings.Azure.get()
                return cls._get(llm=llm, embedding=embedding)

    # Convenience methods
    get_aitomatic_llm = LLMs.Aitomatic.get
    get_openai_llm = LLMs.OpenAI.get
    get_azure_llm = LLMs.Azure.get
