"""
============================
OPENAI LANGUAGE MODELS (LMs)
============================
"""


from __future__ import annotations

from dataclasses import dataclass, field
import json
from multiprocessing import cpu_count
from typing import TYPE_CHECKING

from loguru import logger
from openai import OpenAI  # pylint: disable=import-self
from llama_index.embeddings.openai.base import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from llama_index.llms.openai.base import OpenAI as LlamaIndexOpenAILM

from .base import BaseLM
from .config import LMConfig

if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion
    from .base import LMChatHist


@dataclass
class OpenAILM(BaseLM):
    """OpenAI LM."""

    client: OpenAI = field(init=False)

    def __post_init__(self):
        """Initialize OpenAI client."""
        self.client: OpenAI = OpenAI(api_key=self.api_key, base_url=self.api_base)

    @classmethod
    def from_defaults(cls) -> OpenAILM:
        """Get OpenAI LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(model=LMConfig.OPENAI_DEFAULT_MODEL, api_key=LMConfig.OPENAI_API_KEY, api_base=LMConfig.OPENAI_API_URL)

    def call(self, messages: LMChatHist, **kwargs) -> ChatCompletion:
        """Call OpenAI LM API and return response object."""
        return self.client.chat.completions.create(messages=messages,
                                                   model=self.model,
                                                   seed=kwargs.pop('seed', LMConfig.DEFAULT_SEED),
                                                   temperature=kwargs.pop('temperature', LMConfig.DEFAULT_TEMPERATURE),
                                                   **kwargs)

    def get_response(self, prompt: str, history: LMChatHist | None = None, json_format: bool = False, **kwargs) -> str:
        """Call OpenAI LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({'role': 'user', 'content': prompt})

        if json_format:
            kwargs['response_format'] = {'type': 'json_object'}

            while True:
                try:
                    return json.loads(response := self.call(messages, **kwargs).choices[0].message.content)
                except json.decoder.JSONDecodeError:
                    logger.debug(f'INVALID JSON, TO BE RETRIED:\n{response}')  # pylint: disable=used-before-assignment

        return self.call(messages, **kwargs).choices[0].message.content


def default_llama_index_openai_embed_model() -> OpenAIEmbedding:
    # platform.openai.com/docs/models/embeddings
    return OpenAIEmbedding(mode=OpenAIEmbeddingMode.SIMILARITY_MODE, model=OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE,
                           embed_batch_size=100, dimensions=3072, additional_kwargs=None,
                           api_key=None, api_base=None, api_version=None,
                           max_retries=10, timeout=60,
                           reuse_client=True, callback_manager=None, default_headers=None, http_client=None,
                           num_workers=cpu_count())


def default_llama_index_openai_lm(name: str = LMConfig.OPENAI_DEFAULT_SMALL_MODEL, /) -> LlamaIndexOpenAILM:
    return LlamaIndexOpenAILM(model=name,
                              temperature=LMConfig.DEFAULT_TEMPERATURE,
                              max_tokens=None,
                              additional_kwargs={'seed': LMConfig.DEFAULT_SEED},
                              max_retries=3, timeout=60, reuse_client=True,
                              api_key=None, api_base=None, api_version=None,
                              callback_manager=None, default_headers=None, http_client=None, async_http_client=None,
                              system_prompt=None, messages_to_prompt=None, completion_to_prompt=None,
                              # pydantic_program_mode=...,
                              output_parser=None)
