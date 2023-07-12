"""
This module contains the HuggingFaceBaseSLM class, and its subclasses,
which are SLMs based on models from HugoingFace. The models may be
served from HuggingFace's model hub, or a private internal server,
or they may be served locally.
"""
import json
import ast
import torch

from requests import request
from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM

from openssm.core.slm.base_slm import BaseSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.config import Config


class HuggingFaceBaseSLM(BaseSLM):
    """
    This class is the base class for all SLMs based on models from
    HuggingFace. The models may be served from HuggingFace's model hub,
    or a private internal server, or they may be served locally.
    """
    def __init__(self,
                 model_name=None,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        super().__init__(adapter)
        if model_name is None:
            raise ValueError("model_name must be specified")

        self.local_mode = model_url is None

        if self.local_mode:
            # Load the model and tokenizer from the local cache
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                device_map="auto")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                rust_remote_code=True)
            self.local_model = pipeline(
                "text-generation",
                model=model,
                tokenizer=self.tokenizer,
                torch_dtype=torch.float32,
                trust_remote_code=True,
                device_map="auto"
            )
        else:
            # Require model_url and model_server_token
            if model_url is None:
                raise ValueError("model_url must be specified")
            if model_server_token is None:
                raise ValueError("model_server_token must be specified")
            self.model_url = model_url
            self.model_server_token = model_server_token

    def call_lm_api(self, conversation: list[dict]) -> list[dict]:
        """
        This method calls the API of the underlying language model,
        and returns the response as a list of dicts.
        """
        # Convert conversation to string
        list_conversation = []
        for item in conversation:
            role = item["role"]
            content = item["content"]
            list_conversation.append(f'{role}: {content}')

        prompt = "\n".join(list_conversation)
        # Need to update the prompt
        prompt = (f"Complete this conversation with the assistant’s response, "
                  f"up to 500 words, in JSON, with quotes escaped with \\:\n"
                  f"{prompt}")

        if self.local_mode:
            result = self.local_model(prompt,
                                      max_length=200,
                                      do_sample=True,
                                      top_k=5,
                                      num_return_sequences=1,
                                      eos_token_id=self.tokenizer.eos_token_id)
        else:
            data = json.dumps({"inputs": prompt})
            headers = {
                'Authorization': f'Bearer {self.model_server_token}',
                'Content-Type': 'application/json'
            }
            response = request(method="POST",
                               url=self.model_url,
                               headers=headers,
                               data=data,
                               timeout=10)
            if response.status_code == 200:
                result = ast.literal_eval(response.text.strip())
            else:
                message = 'Model unavailable, try again'
                result = [{'generated_text': message}]

        if not isinstance(result, list):
            result = [result]

        reply = result[0]['generated_text']

        # Return the reply in the same format as the input
        reply_dict = {"role": "assistant", "content": reply}
        return [reply_dict]


class Falcon7bSLM(HuggingFaceBaseSLM):
    """
    Falcon7bSLM is a wrapper for the Falcon7b model, which may be hosted
    locally or remotely. If hosted remotely, the model_url and
    model_server_token must be provided through the Config class.
    """
    def __init__(self,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        model_name = "tiiuae/falcon-7b"
        model_url = model_url or Config.FALCON7B_MODEL_URL
        model_server_token = model_server_token or Config.FALCON7B_SERVER_TOKEN

        super().__init__(model_name=model_name,
                         model_url=model_url,
                         model_server_token=model_server_token,
                         adapter=adapter)


class Falcon7bSLMLocal(HuggingFaceBaseSLM):
    """
    Provided for convenience, this class is a wrapper for the Falcon7b
    model hosted locally.
    """

    def __init__(self,
                 adapter: AbstractAdapter = None):
        super().__init__(model_name="tiiuae/falcon-7b",
                         model_url=None,
                         model_server_token=None,
                         adapter=adapter)
