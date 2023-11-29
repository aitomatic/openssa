"""
This module contains the HuggingFaceBaseSLM class, and its subclasses,
which are SLMs based on models from HugoingFace. The models may be
served from HuggingFace's model hub, or a private internal server.
"""
import os
import json
from typing import Optional
from requests import request
from openssa.core.slm.base_slm import BaseSLM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.utils.config import Config
from openssa.utils.logs import Logs


Config.FALCON7B_API_KEY: Optional[str] = os.environ.get('FALCON7B_API_KEY')
Config.FALCON7B_API_URL: Optional[str] = os.environ.get('FALCON7B_API_URL')


class SLM(BaseSLM):
    """
    This class is the base class for all SLMs based on models from
    HuggingFace. The models may be served from HuggingFace's model hub,
    or a private internal server.

    model_url should be set appropriately:
    - If hosted on HuggingFace, set to the model's URL on HuggingFace.
    - If hosted on AWS/GCP, set to the model's URL on there
    - If not supported, set to "NONE" (or not set at all)
    """

    _not_supported = False

    def __init__(self,
                 model_name=None,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        super().__init__(adapter)
        if model_name is None:
            raise ValueError("model_name must be specified")

        self._not_supported = model_url is None or model_url == "NONE"

        if self._not_supported:
            return

        # Require model_url and model_server_token
        if model_url is None:
            raise ValueError("model_url must be specified")
        if model_server_token is None:
            raise ValueError("model_server_token must be specified")
        self.model_url = model_url
        self.model_server_token = model_server_token

    @Logs.do_log_entry_and_exit()
    def _call_lm_api(self, conversation: list[dict]) -> dict:
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
            return reply_dict

        prompt = self._make_completion_prompt(conversation)

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
            response_text = response.text.strip()
            response_dict = json.loads(response_text)
            if isinstance(response_dict, list):
                response_dict = response_dict[0]

            result = self._parse_llm_response(response_text)
        else:
            message = 'Model unavailable, try again'
            result = {'system': message}

        return result


class Falcon7bSLM(SLM):
    """
    Falcon7bSLM is a wrapper for the Falcon7b model, which may be hosted
    remotely. If hosted remotely, the model_url and
    model_server_token must be provided through the Config class.

    FALCON7B_API_URL should be set appropriately:
    - If hosted on HuggingFace, set to the model's URL on HuggingFace.
    - If hosted on AWS/GCP, set to the model's URL on there
    - If not supported, set to "NONE" (or not set at all)
    """

    def __init__(self,
                 model_url=None,
                 model_server_token=None,
                 adapter: AbstractAdapter = None):

        model_name = "tiiuae/falcon-7b"
        model_url = model_url or Config.FALCON7B_API_URL or "NONE"
        model_server_token = model_server_token or Config.FALCON7B_API_KEY

        super().__init__(model_name=model_name,
                         model_url=model_url,
                         model_server_token=model_server_token,
                         adapter=adapter)
