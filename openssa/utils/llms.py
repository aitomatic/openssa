from __future__ import annotations
from typing import Optional
import os
import json
from openai import OpenAI, AzureOpenAI
from openssa.utils.config import Config

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


class AnLLM():
    """
    This class provides a consistent API for the different LLM services.
    Intended usage:

        from openssa.utils.llms import OpenAILLM, AitomaticLLM, AzureLLM

        llm1 = OpenAILLM.get_default()
        llm1.call(messages=[{"role": "user", "content": "Say this is a test"}], stream=True)
        llm1.create_embeddings()

        llm2 = AitomaticLLM.get_default()
        llm3 = AitoLLM.get_gpt_35_turbo_0613()

        llm4 = AzureLLM.get_default()

    etc.
    """

    def __init__(
        self,
        model: str = None,
        api_base: str = None,
        api_key: str = None,
        **additional_kwargs,
    ):
        self.model = model
        self.api_base = api_base
        self.api_key = api_key
        self._client = None
        self._additional_kwargs = additional_kwargs

    @property
    def client(self):
        pass

    def call(self, is_chat: bool = True, **kwargs):
        if is_chat:
            result = self.client.chat.completions.create(
                model=self.model, **kwargs, **self._additional_kwargs
            )
        else:
            result = self.client.completions.create(
                model=self.model, **kwargs, **self._additional_kwargs
            )
        return result

    def create_embeddings(self):
        return self.client.embeddings.create(model=self.model)

    def get_response(self, prompt: str, history: list = None, **kwargs) -> str:
        messages = history or []
        messages.append({"role": "user", "content": prompt})
        return self.call(messages=messages, **kwargs).choices[0].message.content

    def parse_output(self, output: str) -> dict:
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            print("Failed to decode the response as JSON.")
            return {}


class OpenAILLM(AnLLM):
    """
    This class represents the OpenAI-hosted LLMs
    """

    def __init__(
        self,
        model: str = None,
        api_base: str = None,
        api_key: str = None,
        **additional_kwargs,
    ):
        if model is None:
            model = "gpt-3.5-turbo-1106"
        if api_base is None:
            api_base = Config.OPENAI_API_URL
        if api_key is None:
            api_key = Config.OPENAI_API_KEY
        super().__init__(
            model=model, api_base=api_base, api_key=api_key, **additional_kwargs
        )

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        return self._client

    @classmethod
    def get_default(cls) -> OpenAILLM:
        return cls.get_gpt_35_turbo()

    @classmethod
    def get_gpt_35_turbo_1106(cls) -> OpenAILLM:
        return cls(model="gpt-3.5-turbo-1106")

    @classmethod
    def get_gpt_35_turbo_0613(cls) -> OpenAILLM:
        return cls(model="gpt-3.5-turbo")

    @classmethod
    def get_gpt_35_turbo(cls) -> OpenAILLM:
        return cls(model="gpt-3.5-turbo-0613")

    @classmethod
    def get_gpt_4(cls) -> OpenAILLM:
        return cls(model="gpt-4")

    @classmethod
    def get_gpt_4_1106_preview(cls) -> OpenAILLM:
        return cls(model="gpt-4-1106-preview")


class AitomaticLLM(OpenAILLM):
    """
    This class represents the Aitomatic-hosted LLMs
    """

    def __init__(
        self,
        model: str = None,
        api_base: str = None,
        api_key: str = None,
        **additional_kwargs,
    ):
        if model is None:
            model = "llama2-7b"
        if api_base is None:
            api_base = Config.AITOMATIC_API_URL
        if api_key is None:
            api_key = Config.AITOMATIC_API_KEY
        super().__init__(
            model=model, api_base=api_base, api_key=api_key, **additional_kwargs
        )

    @classmethod
    def get_default(cls) -> AitomaticLLM:
        return cls.get_llama2_7b()

    @classmethod
    def get_llama2_70b(cls) -> AitomaticLLM:
        # TODO: there should be a single Aitomatic api_base and api_key
        return cls(
            model="llama2-70b",
            api_base=Config.AITOMATIC_API_URL_70B,
            api_key=Config.LEPTON_API_KEY,
        )

    @classmethod
    def get_llama2_7b(cls) -> AitomaticLLM:
        # TODO: there should be a single Aitomatic api_base and api_key
        return cls(
            model="llama2-7b",
            api_base=Config.AITOMATIC_API_URL_70B,
            api_key=Config.LEPTON_API_KEY,
        )

    @classmethod
    def get_13b(cls) -> AitomaticLLM:
        # TODO: there should be a single Aitomatic api_base and api_key
        return cls(
            model="gpt-3.5-turbo-0613",
            api_base="http://35.199.34.91:8000/v1",
            api_key=Config.AITOMATIC_API_KEY,
        )

    @classmethod
    def get_yi_34b(cls) -> AitomaticLLM:
        # TODO: there should be a single Aitomatic api_base and api_key
        return cls(
            model="01-ai/Yi-34B-Chat",
            api_base="http://35.230.174.89:8000/v1",
            additional_kwargs={"stop": "\n###"},
        )

    @classmethod
    def get_intel_neural_chat_7b(cls) -> AitomaticLLM:  # running
        # TODO: there should be a single Aitomatic api_base and api_key
        return cls(
            model="Intel/neural-chat-7b-v3-1", api_base="http://34.145.174.152:8000/v1"
        )


class AzureLLM(AnLLM):
    """
    This class represents the Azure-hosted LLMs
    """

    def __init__(self, model: str = None, api_base: str = None, api_key: str = None):
        if model is None:
            model = "gpt-35-turbo"
        if api_base is None:
            api_base = Config.AZURE_OPENAI_API_URL
        if api_key is None:
            api_key = Config.AZURE_OPENAI_API_KEY
        super().__init__(model=model, api_base=api_base, api_key=api_key)

    @property
    def client(self) -> AzureOpenAI:
        if self._client is None:
            self._client = AzureOpenAI(
                api_key=self.api_key, azure_endpoint=self.api_base
            )
        return self._client

    @classmethod
    def get_default(cls) -> AzureLLM:
        return cls.get_gpt_35()

    @classmethod
    def get_gpt_35(cls) -> AzureLLM:
        return cls(model="gpt-35-turbo")

    @classmethod
    def get_gpt_35_16k(cls) -> AzureLLM:
        return cls(model="gpt-35-turbo-16k")

    @classmethod
    def get_gpt_4(cls) -> AzureLLM:
        return cls(model="gpt-4-32k")
