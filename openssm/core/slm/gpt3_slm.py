from core.config import Config
from .base_slm import BaseSLM
from core.adapter.abstract_adapter import AbstractAdapter
from abc import abstractmethod
import openai
import ast


class GPT3BaseSLM(BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)
        openai.api_key = Config.OPENAI_API_KEY
        self.conversations = {}  # dict of conversation_id: list of messages

    @abstractmethod
    def call_openai(self, conversation: list[dict]) -> list[dict]:
        """Call OpenAI's API and return the response"""
        pass

    def discuss(self,
                conversation_id: str,
                user_input: list[dict]) -> list[dict]:
        """Send user input to OpenAI's API and return the replies"""

        # If conversation is new, start a new one, else continue from previous
        conversation = self.conversations.get(conversation_id, [])
        conversation.extend(user_input)

        replies = self.call_openai(conversation)

        # Save response to the conversation
        conversation.extend(replies)
        self.conversations[conversation_id] = conversation

        # Return the model's replies
        return replies

    def reset_memory(self):
        # Clear all conversations
        self.conversations = {}


class GPT3CompletionSLM(GPT3BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)

    def call_openai(self, conversation: list[dict]) -> list[dict]:
        # Convert conversation to string
        list_conversation = []
        for item in conversation:
            role = item["role"].replace('"', '\\"')
            content = item["content"].replace('"', '\\"')
            list_conversation.append(
                f'{{"role": "{role}", "content": "{content}"}}'
            )

        prompt = "\n".join(list_conversation)
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


class GPT3ChatCompletionSLM(GPT3BaseSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        super().__init__(adapter)

    def call_openai(self, conversation: list[dict]) -> list[dict]:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            # max_tokens=150,
            temperature=0.7
        )
        return [response.choices[0].message]
