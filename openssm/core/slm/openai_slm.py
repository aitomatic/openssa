import openai
from openssm.core.slm.base_slm import BaseSLM
from openssm.config import Config
from openssm.core.adapter.abstract_adapter import AbstractAdapter


class GPT3BaseSLM(BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)
        if Config.OPENAI_API_KEY is None:
            raise ValueError("Config.OPENAI_API_KEY is not set")
        openai.api_key = Config.OPENAI_API_KEY


class GPT3ChatCompletionSLM(GPT3BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)

    def call_lm_api(self, conversation: list[dict]) -> list[dict]:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            # max_tokens=150,
            temperature=0.7
        )
        return [response.choices[0].message]


class GPT3CompletionSLM(GPT3BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)

    def call_lm_api(self, conversation: list[dict]) -> list[dict]:
        prompt = self._make_completion_prompt(conversation)

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )
        # print(f"prompt: {prompt}")
        # print(f"response: {response}")
        response = response.choices[0].text.strip()

        replies = self._parse_llm_response(response)

        if len(replies) == 0 or len(replies[0]) == 0:
            replies = [{'role': 'assistant', 'content': 'I got nothing.'}]

        # print(f"replies: {replies}")

        return replies
