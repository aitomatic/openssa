from .abstract_slm import AbstractSLM
from ..adapter.abstract_adapter import AbstractAdapter


class BaseSLM(AbstractSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        """
        self.conversations is initialized as a dictionary of conversations,
        where each conversation is a list of user inputs and model replies.
        """
        self.adapter = adapter
        self.conversations = {}

    def get_adapter(self) -> AbstractAdapter:
        return self.adapter

    def set_adapter(self, adapter: AbstractAdapter):
        self.adapter = adapter

    def discuss(self,
                conversation_id: str,
                user_input: list[dict]) -> list[dict]:
        """
        Send user input to OpenAI's API and return the replies
        """

        # If conversation is new, start a new one, else continue from previous
        conversation = self.conversations.get(conversation_id, [])
        conversation.extend(user_input)

        replies = self.call_lm_api(conversation)

        # Save response to the conversation
        conversation.extend(replies)
        self.conversations[conversation_id] = conversation

        # Return the model's replies
        return replies

    def reset_memory(self):
        self.conversations = {}
