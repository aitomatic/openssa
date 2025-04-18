from __future__ import annotations

from dataclasses import dataclass, field
import json
import time
from typing import TYPE_CHECKING
from loguru import logger

from openai import AzureOpenAI
from openssa.core.util.lm.base import BaseLM
from .config import LMConfig


if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion
    from openssa.core.util.lm.base import LMChatHist


@dataclass
class AzureOpenAILM(BaseLM):
    """OpenAI LM."""

    azure_endpoint: str = ''
    api_version: str = LMConfig.AZURE_OPENAI_API_VERSION
    client: AzureOpenAI = field(init=False)

    def __post_init__(self):
        """Initialize OpenAI client."""
        self.client: AzureOpenAI = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )

    @classmethod
    def from_defaults(cls) -> AzureOpenAILM:
        """Get OpenAI LM instance with default parameters."""
        # pylint: disable=unexpected-keyword-arg
        return cls(
            model=LMConfig.AZURE_OPENAI_GPT_MODEL_NAME,
            api_base=None,
            api_key=LMConfig.AZURE_OPENAI_API_KEY,
            azure_endpoint=LMConfig.AZURE_OPENAI_ENDPOINT,
        )

    def call(self, messages: LMChatHist, **kwargs) -> ChatCompletion:
        """Call OpenAI LM API and return response object."""
        return self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            seed=kwargs.pop("seed", LMConfig.DEFAULT_SEED),
            temperature=kwargs.pop("temperature", LMConfig.DEFAULT_TEMPERATURE),
            **kwargs,
        )

    def get_response(
        self,
        prompt: str,
        history: LMChatHist | None = None,
        json_format: bool = False,
        **kwargs,
    ) -> str:
        """Call OpenAI LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({"role": "user", "content": prompt})

        if json_format:
            kwargs["response_format"] = {"type": "json_object"}

            """
            The json_format is set to false by default
            if true, it retries up to five times with amplified retry times.
            """
            MAX_RETRIES = 5
            retries = 0
            backoff = 1

            while retries < MAX_RETRIES:
                try:
                    logger.info(f"RETRIES: {retries}")
                    return json.loads(
                        response := self.call(messages, **kwargs)
                        .choices[0]
                        .message.content
                    )
                except json.decoder.JSONDecodeError:
                    retries += 1
                    logger.debug(
                        f"INVALID JSON, TO BE RETRIED ({retries}/{MAX_RETRIES}):\n{response}"
                    )
                    time.sleep(backoff)
                    backoff *= 2

            raise ValueError("Max retries reached. Unable to parse JSON response.")

        return self.call(messages, **kwargs).choices[0].message.content
