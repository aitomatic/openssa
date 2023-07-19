"""
This module contains the HuggingFaceBaseSLM class, and its subclasses,
which are SLMs based on models from HugoingFace. The models may be
served from HuggingFace's model hub, or a private internal server,
or they may be served locally.
"""
import json
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

    If local, `model_url` must be explicitly set to "LOCAL". This
    is to avoid accidentally using a local model, which consumes a lot
    of resources, when the user intended to use a model from a hosted server.

    model_url should be set appropriately:
    - If hosted on HuggingFace, set to the model's URL on HuggingFace.
    - If hosted on AWS/GCP, set to the model's URL on there
    - If hosted locally, set to "LOCAL"
    - If not supported, set to "NONE" (or not set at all)
    """

    _not_supported = False
    _local_mode = False

    def __init__(self,
                 model_name=None,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        super().__init__(adapter)
        if model_name is None:
            raise ValueError("model_name must be specified")

        self._local_mode = model_url == "LOCAL"
        self._not_supported = model_url is None or model_url == "NONE"

        if self._not_supported:
            return

        if self._local_mode:
            # Load the model and tokenizer from the local cache
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                device_map="auto")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True)
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
        if self._not_supported:
            reply_dict = {
                "role": "assistant",
                "content":
                f"Sorry, {self.__class__.__name__} model is unsupported."
            }
            return [reply_dict]

        prompt = self._make_completion_prompt(conversation)
        # print(f"prompt: {prompt}")

        if self._local_mode:
            result = self.local_model(prompt,
                                      max_length=2000,
                                      do_sample=True,
                                      top_k=5,
                                      num_return_sequences=1,
                                      eos_token_id=self.tokenizer.eos_token_id)
        else:
            data = json.dumps({"inputs": prompt})
            headers = {'Content-Type': 'application/json'}

            if 'amazonaws' in self.model_url or 'aitomatic' in self.model_url:
                headers['x-api-key'] = self.model_server_token
            else:
                headers['Authorization'] = f'Bearer {self.model_server_token}'

            response = request(method="POST",
                               url=self.model_url,
                               headers=headers,
                               data=data,
                               timeout=10)

            if response.status_code == 200:
                # pylint: disable=invalid-name
                responseText = response.text.strip()
                responseDict = json.loads(responseText)
                if isinstance(responseDict, list):
                    responseDict = responseDict[0]

                result = self._parse_llm_response(responseText)
            else:
                message = 'Model unavailable, try again'
                result = [{'system': message}]

        # print(f"result: {result}")
        return result


class Falcon7bSLM(HuggingFaceBaseSLM):
    """
    Falcon7bSLM is a wrapper for the Falcon7b model, which may be hosted
    locally or remotely. If hosted remotely, the model_url and
    model_server_token must be provided through the Config class.

    FALCON7B_MODEL_URL should be set appropriately:
    - If hosted on HuggingFace, set to the model's URL on HuggingFace.
    - If hosted on AWS/GCP, set to the model's URL on there
    - If hosted locally, set to "LOCAL"
    - If not supported, set to "NONE" (or not set at all)
    """

    def __init__(self,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        model_name = "tiiuae/falcon-7b"
        model_url = model_url or Config.FALCON7B_MODEL_URL or "NONE"
        model_server_token = model_server_token or Config.FALCON7B_SERVER_TOKEN

        super().__init__(model_name=model_name,
                         model_url=model_url,
                         model_server_token=model_server_token,
                         adapter=adapter)


class Falcon7bSLMLocal(Falcon7bSLM):
    """
    Provided for convenience, this class is a wrapper for the Falcon7b
    model hosted locally.
    """

    def __init__(self,
                 adapter: AbstractAdapter = None):
        super().__init__(model_url="LOCAL",
                         model_server_token=None,
                         adapter=adapter)
