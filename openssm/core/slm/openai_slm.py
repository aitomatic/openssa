import ast
import openai
from ...config import Config
from .base_slm import BaseSLM
from ..adapter.abstract_adapter import AbstractAdapter


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

    def convert_conversation_to_string(self, conversation: list[dict]) -> str:
        list_conversation = []
        for item in conversation:
            role = item["role"].replace('"', '\\"')
            content = item["content"].replace('"', '\\"')
            list_conversation.append(
                f'{{"role": "{role}", "content": "{content}"}}'
            )
        return ", ".join(list_conversation)

    def call_lm_api(self, conversation: list[dict]) -> list[dict]:
        prompt = self.convert_conversation_to_string(conversation)
        prompt = (f"Complete this conversation with the assistant’s response, "
                  f"up to 500 words, in JSON, with quotes escaped with \\:\n"
                  f"{prompt}")

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].text.strip()
        reply_dict = ast.literal_eval(reply)
        return [reply_dict]
