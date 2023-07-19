import json
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter


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

    # pylint: disable=unused-argument
    def call_lm_api(self, conversation: list[dict]) -> list[dict]:
        """
        Send conversation to the language model’s API
        and return the replies. Should be overridden by subclasses.
        """
        response = '{"assistant": "Hello, how can I help you?"}'
        return self._parse_llm_response(response)

    def reset_memory(self):
        self.conversations = {}

    #
    # Helper functions for GPT-like completion models
    #
    def _make_completion_prompt(self, conversation: list[dict]) -> str:
        # print(f"conversation: {conversation}")
        prompt = self._convert_conversation_to_string(conversation)
        prompt = ("Complete this conversation with the response, " +
                  "up to 2000 words (plus this prompt): " +
                  "{'role': 'assistant', 'content': 'xxx'} format. " +
                  "where 'xxx' is the response. " +
                  "Make sure the entire response is valid JSON, xxx is " +
                  "only a string, and no code of any kind, even if the " +
                  "prompt has code. " +
                  "Escape quotes with \\:\n" +
                  f"{prompt}")
        return prompt

    def _convert_conversation_to_string(self, conversation: list[dict]) -> str:
        list_conversation = []
        for item in conversation:
            # print(f"item: {item}")
            role = item["role"].replace('"', '\\"')
            content = item["content"].replace('"', '\\"')
            list_conversation.append(
                f'{{"role": "{role}", "content": "{content}"}}'
            )
        return ", ".join(list_conversation)

    def _old_parse_llm_response(self, response) -> list[dict]:
        response = response.strip()
        valid_json_strings = []
        start_index = 0
        end_index = len(response)

        while start_index < end_index:
            try:
                json_string = response[start_index:end_index]
                json.loads(json_string)  # Verify the JSON validity
                valid_json_strings.append(json_string)
                start_index += len(json_string)
                end_index = len(response)
            except (ValueError, json.JSONDecodeError):
                end_index -= 1

        parsed_data = []
        for json_string in valid_json_strings:
            try:
                item = json.loads(json_string)
                if isinstance(item, list):
                    parsed_data.extend(item)
                else:
                    parsed_data.append(item)
            except (ValueError, json.JSONDecodeError):
                print(f"Invalid JSON string: {json_string}")
                pass

        if isinstance(parsed_data, list):
            return parsed_data

        return [parsed_data]

    def _parse_llm_response(self, response) -> list[dict]:
        response = response.strip()

        if response.startswith('{') and not response.endswith('}'):
            response += '}'

        if response.endswith('}') and not response.startswith('{'):
            response += '{'

        if '{' not in response:
            response = json.dumps({"assistant": response})

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
