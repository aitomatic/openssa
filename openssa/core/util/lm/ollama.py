"""
=================================
HUGGINGFACE LANGUAGE MODELS (LMs)
=================================
"""


from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import TYPE_CHECKING

from loguru import logger

from llama_index.llms.ollama import Ollama, ChatResponse
from llama_index.llms.base import FunctionCallingLLM, LLMMetadata
from typing import List

from .base import BaseLM
from .config import LMConfig


if TYPE_CHECKING:
    from llama_index.core.chat_engine.types import AgentChatResponse
    from llama_index.core.tools.types import BaseTool


@dataclass
class OllamaLM(BaseLM):
    """Wrapper for OLLAMA using llama-index API."""

    def __init__(self, model: str, request_timeout: float = 60.0, **kwargs):
        """
        Initialize the OLLAMA wrapper.

        Args:
            model (str): The model name (e.g., "llama2").
            request_timeout (float): Request timeout for API calls, in seconds.
            **kwargs: Additional arguments passed to the OLLAMA client.
        """
        super().__init__()
        self.llm = Ollama(model=model, request_timeout=request_timeout, **kwargs)

    @property
    def metadata(self) -> LLMMetadata:
        """
        Return metadata about the LLM.

        Returns:
            LLMMetadata: Metadata about the LLM (e.g., model name, supported features).
        """
        return self.llm.metadata

    def call(self, messages: LMChatHist, **kwargs) -> ChatCompletion:
        """
        Generate a completion for a given prompt.

        Args:
            prompt (str): The input prompt.
            **kwargs: Additional arguments for the LLM completion.

        Returns:
            str: The generated text completion.
        """
        response = self.llm.complete(messages, **kwargs)
        return response

    def get_tool_calls_from_response(self, response: ChatResponse, error_on_no_tool_call: bool = True) -> List[ToolSelection]:
        """
        Extract and process tool calls from a response.

        Args:
            response (ChatResponse): The chat response to process.
            error_on_no_tool_call (bool): Whether to raise an error if no tool call is found.

        Returns:
            List[ToolSelection]: The list of tools selected from the response.
        """
        return self.llm.get_tool_calls_from_response(response, error_on_no_tool_call=error_on_no_tool_call)

    def get_response(self, prompt: str, history: List[dict] = None, json_format: bool = False, **kwargs) -> str:
        """
        Generate a response to a user prompt using the LLM.

        Args:
            prompt (str): The user input prompt.
            history (List[dict], optional): Chat history to maintain context. Defaults to None.
            json_format (bool): Whether to attempt parsing the response as JSON. Defaults to False.
            **kwargs: Additional arguments for the LLM completion.

        Returns:
            str: The LLM's response or the parsed JSON content.
        """
        messages = history or []
        messages.append({"role": "user", "content": prompt})

        if json_format:
            while True:
                try:
                    response = self.llm.call(messages, **kwargs)
                    return json.loads(response)  # Ensure response is valid JSON
                except json.JSONDecodeError:
                    logger.debug(f"INVALID JSON, TO BE RETRIED:\n{response}")
        else:
            response = self.llm.call(messages, **kwargs)
            return response

