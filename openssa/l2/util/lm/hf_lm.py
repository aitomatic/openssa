import asyncio
import requests
import nest_asyncio


class HFLlamaLM:
    """
    Wrapper class to run Huggingface's Serverless Inference API for Llama3
    """
    def __init__(self, api_token, model='meta-llama/Meta-Llama-3-8B-Instruct'):
        """
        Initialize the LlamaHFWrapper instance with the given API token and model.

        :param api_token: Hugging Face API token.
        :param model: The model identifier from Hugging Face.
        """
        self.hostname = 'https://api-inference.huggingface.co'
        self.domain_path = f'/models/{model}'
        self.api_token = api_token
        self.headers = {'Authorization': f'Bearer {self.api_token}'}

        # Apply nest_asyncio to enable nested usage of asyncio's event loop
        nest_asyncio.apply()

        # Add an asyncio queue for streaming responses
        self.queue = asyncio.Queue()

    def run_sync(self, api_request_json):
        """
        Run the synchronous request to the API.

        :param api_request_json: The JSON request payload for the API.
        :return: The JSON response from the API.
        """
        # pylint: disable=W3101:missing-timeout
        response = requests.post(f"{self.hostname}{self.domain_path}", headers=self.headers, json=api_request_json)  # noqa: S113
        # pylint: enable
        print(f"error code = {response.status_code}")
        if response.status_code != 200:
            # pylint: disable=W0719:broad-exception-raised
            raise Exception(f"POST {response.status_code} {response.json().get('error', response.text)}")  # noqa: TRY002
            # pylint: enable
        return response.json()

    def run(self, api_request_json):
        """
        Run the request based on the presence of streaming in the JSON payload.

        :param api_request_json: The JSON request payload for the API.
        :return: The response from the appropriate method (streaming or synchronous).
        """
        return self.run_sync(api_request_json)
