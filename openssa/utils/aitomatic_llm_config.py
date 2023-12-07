import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


class AitomaticLLMConfig:
    @classmethod
    def get_llama2_70b(cls):
        return OpenAI(
            api_key=os.environ.get("LEPTON_API_KEY", "twoun3dz0fzw289dgyp2rlb3kltti8zi"),
            base_url="https://llama2-70b.lepton.run/api/v1",
        )

    @classmethod
    def get_intel_neural_chat_7b(cls):
        url_base = os.environ.get(
            "AITOMATIC_INTEL_NEURAL_CHAT_7B_URL_BASE", "http://34.145.174.152:8000/v1"
        )
        llm = OpenAI(base_url=url_base)
        return llm

    @classmethod
    def get_aimo_llm(cls):
        url_base = os.environ.get("AIMO_STANDARD_URL_BASE")
        llm = OpenAI(
            base_url=url_base,
        )
        return llm

    @classmethod
    def get_openai(cls):
        return OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
        )

    @classmethod
    def get_aitomatic_llm(cls):
        return OpenAI(
            api_key=os.environ.get("AITOMATIC_API_KEY", "AITOMATIC"),
            base_url="https://aimo-api-mvp.platform.aitomatic.com/api/v1",
        )
