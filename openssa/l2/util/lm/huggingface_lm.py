"""
============================
HUGGINGFACE LANGUAGE MODELS (LMs)
============================
"""


from __future__ import annotations

from dataclasses import dataclass, field
import json
from multiprocessing import cpu_count
from typing import TYPE_CHECKING

# from openai import OpenAI  # pylint: disable=import-self
from huggingface_hub.inference._client import InferenceClient
from llama_index.embeddings.openai.base import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from llama_index.llms.openai.base import OpenAI as LlamaIndexOpenAILM, DEFAULT_OPENAI_MODEL

from .abstract import AbstractLM, LMChatHist
from .config import LMConfig

if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion


@dataclass
class HuggingFaceLM(AbstractLM):
    """HuggingFace LM."""

    # client: OpenAI = field(init=False)
    client: InferenceClient = field(init=False)

    def __post_init__(self):
        """Initialize HuggingFace client."""
        # self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.api_base)
        print("Initialized LM through HF!")
        print(f"LMConfig.HF_API_KEY = {LMConfig.HF_API_KEY}")
        self.client: InferenceClient = InferenceClient(model=LMConfig.DEFAULT_HF_LLAMA_MODEL, token=LMConfig.HF_API_KEY)

    @classmethod
    def from_defaults(cls) -> HuggingFaceLM:
        """Get HuggingFace LM instance with default parameters."""
        # # pylint: disable=unexpected-keyword-arg
        # return cls(model=LMConfig.DEFAULT_OPENAI_MODEL, api_key=LMConfig.OPENAI_API_KEY, api_base=LMConfig.OPENAI_API_URL)
        # pylint: disable=unexpected-keyword-arg
        print("Initialized Default LM through HF!")

        return cls(model=LMConfig.DEFAULT_HF_LLAMA_MODEL, api_key=LMConfig.HF_API_KEY, api_base=LMConfig.HF_API_URL)

    def call(self, messages: LMChatHist, **kwargs) -> ChatCompletion:
        """Call HuggingFace LM API and return response object."""
        # return self.client.chat.completions.create(model=self.model,
        #                                            messages=messages,
        #                                            seed=kwargs.pop('seed', LMConfig.DEFAULT_SEED),
        #                                            temperature=kwargs.pop('temperature', LMConfig.DEFAULT_TEMPERATURE),
        #                                            **kwargs)
        print("HF LM Call performed!")
        return self.client.chat_completion(
            model=self.model,
            messages=messages,
            seed=kwargs.pop('seed', LMConfig.DEFAULT_SEED),
            temperature=kwargs.pop('temperature', LMConfig.DEFAULT_TEMPERATURE),
            **kwargs)

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call HuggingFace LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})

        # if json_format:
        #     kwargs['response_format'] = {'type': 'json_object'}

        response_content: str = self.call(messages, **kwargs).choices[0].message.content
        print(f"HF response_content = {response_content}")

        # return json.loads(response_content) if json_format else response_content
        return response_content


def default_llama_index_openai_embed_model() -> OpenAIEmbedding:
    return OpenAIEmbedding(mode=OpenAIEmbeddingMode.SIMILARITY_MODE, model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE,
                           embed_batch_size=100, dimensions=3072, additional_kwargs=None,
                           api_key=None, api_base=None, api_version=None,
                           max_retries=10, timeout=60,
                           reuse_client=True, callback_manager=None, default_headers=None, http_client=None,
                           num_workers=cpu_count())


def default_llama_index_openai_lm() -> LlamaIndexOpenAILM:
    return LlamaIndexOpenAILM(model=DEFAULT_OPENAI_MODEL,
                              temperature=LMConfig.DEFAULT_TEMPERATURE,
                              max_tokens=None,
                              additional_kwargs={'seed': LMConfig.DEFAULT_SEED},
                              max_retries=3, timeout=60, reuse_client=True,
                              api_key=None, api_base=None, api_version=None,
                              callback_manager=None, default_headers=None, http_client=None, async_http_client=None,
                              system_prompt=None, messages_to_prompt=None, completion_to_prompt=None,
                              # pydantic_program_mode=...,
                              output_parser=None)
