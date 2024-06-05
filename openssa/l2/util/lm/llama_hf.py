from __future__ import annotations

from dataclasses import dataclass, field

from openssa.l2.util.lm.abstract import AbstractLM, LMChatHist
from openssa.l2.util.lm.config import LMConfig
from openssa.l2.util.lm.openAI_to_HF_prompt_format import build_llama3_prompt

from openssa.l2.util.lm.hf_lm import HFLlamaLM


@dataclass
class LlamaLM(AbstractLM):
    """Llama LM."""

    def __init__(self, model=LMConfig.DEFAULT_HF_LLAMA_MODEL):
        # self.super.__init__()
        self.client: HFLlamaLM = HFLlamaLM(
            api_token="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", model=model
        )

    def get_response(
        self,
        prompt: str,
        history: LMChatHist | None = None,
        json_format: bool = False,
        **kwargs,
    ) -> str:
        # pylint: disable=unused-argument
        """Call Llama LM API and return response content."""
        messages: LMChatHist = history or []
        messages.append({"role": "user", "content": prompt})
        llama_hf_prompt = build_llama3_prompt(messages=messages)
        request_json_sync = {
            "inputs": f"{llama_hf_prompt}",
            "parameters": dict(kwargs),
            "stream": True,
        }

        response = self.client.run(request_json_sync)
        return response
