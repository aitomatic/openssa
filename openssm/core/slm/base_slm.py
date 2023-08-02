import json
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.utils.utils import Utils
from openssm.utils.logs import Logs


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

    @Utils.do_canonicalize_user_input('user_input')
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        Send user input to our language model and return the replies
        """
        # If conversation is new, start a new one, else continue from previous
        conversation = self.conversations.get(conversation_id, [])
        conversation.extend(user_input)

        replies = self._call_lm_api(conversation)
        replies = Utils.canonicalize_query_response(replies)

        # Save response to the conversation
        conversation.extend(replies)
        self.conversations[conversation_id] = conversation

        # Return the model's replies
        return replies

    def reset_memory(self):
        self.conversations = {}

    # pylint: disable=unused-argument
    def _call_lm_api(self, conversation: list[dict]) -> list[dict]:
        """
        Send conversation to the language model’s API
        and return the replies. Should be overridden by subclasses.
        """
        return [{"role": "assistant", "content": "Hello, how can I help you?"}]

    #
    # Helper functions for GPT-like completion models
    #
    @Logs.do_log_entry_and_exit()
    def _make_completion_prompt(self, conversation: list[dict]) -> str:
        system = (
            "Complete this conversation with the assistant’s response, up to 2000 words."
            " Use this format: {\"role\": \"assistant\", \"content\": \"xxx\"},"
            " where 'xxx' is the response."
            " Make sure the entire response is valid JSON, xxx is only a string,"
            " and no code of any kind, even if the prompt has code."
            " Escape quotes with \\:\n"
        )
        system = {"role": "system", "content": system}
        conversation = [system] + conversation
        prompt = str(conversation)
        # prompt = self._convert_conversation_to_string(conversation)
        # pylint: disable=pointless-string-statement
        """
        prompt = ("Complete this conversation with the response, "
                  "up to 2000 words (plus this prompt): "
                  "{'role': 'assistant', 'content': 'xxx'} format. "
                  "where 'xxx' is the response. "
                  "Make sure the entire response is valid JSON, xxx is "
                  "only a string, and no code of any kind, even if the "
                  "prompt has code. "
                  "Escape quotes with \\:\n"
                  f"{prompt}")
        """
        return prompt

    def _convert_conversation_to_string(self, conversation: list[dict]) -> str:
        list_conversation = []
        for item in conversation:
            role = item["role"].replace('"', '\\"')
            content = item["content"].replace('"', '\\"')
            list_conversation.append(
                f'{{"role": "{role}", "content": "{content}"}}'
            )
        return ", ".join(list_conversation)

    def _parse_llm_response(self, response) -> list[dict]:
        response = response.strip()

        if response.startswith('{') and not response.endswith('}'):
            response += '}'

        if response.endswith('}') and not response.startswith('{'):
            response += '{'

        if '{' not in response:
            response = json.dumps({"role": "assistant", "content": response})

        parsed_data = []
        start_indices = [i for i, c in enumerate(response) if c == '{']

        for start in start_indices:
            for end in range(start + 2, len(response) + 1):
                try:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    if isinstance(data, dict):
                        parsed_data.append(data)
                        break
                except json.JSONDecodeError:
                    continue

        return parsed_data

    def save(self, storage_dir: str):
        """Saves to the specified directory."""
        pass

    def load(self, storage_dir: str):
        """Loads from the specified directory."""
        pass


class PassthroughSLM(BaseSLM):
    """
    The PassthroughSLM is a barebones SLM that simply passes
    all queries to the adapter.
    """
    @Utils.do_canonicalize_user_input_and_query_response('user_input')
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        Pass through user input to the adapter and return the replies
        """
        return self.get_adapter().query(user_input, conversation_id)
