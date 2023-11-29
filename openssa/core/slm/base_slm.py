import json
from openssa.core.adapter.base_adapter import BaseAdapter
from openssa.core.slm.abstract_slm import AbstractSLM
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.utils.utils import Utils
from openssa.utils.logs import Logs
from openssa.core.prompts import Prompts


class BaseSLM(AbstractSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        """
        self.conversations is initialized as a dictionary of conversations,
        where each conversation is a list of user inputs and model replies.
        """
        self._adapter = adapter

    @property
    def adapter(self) -> AbstractAdapter:
        """
        Return the previous assigned Adapter,
        or a default Adapter if none was assigned.
        """
        if self._adapter is None:
            self._adapter = BaseAdapter()
        return self._adapter

    @adapter.setter
    def adapter(self, adapter: AbstractAdapter):
        self._adapter = adapter

    def do_discuss(self, user_input: list[dict], conversation: list[dict]) -> dict:
        """
        Add the user_input to the conversation, sends the whole conversation
        to the language model, and returns the reply.
        """
        conversation.extend(user_input)
        result = self._call_lm_api(conversation)
        conversation.pop()
        return result

    # pylint: disable=unused-argument
    def _call_lm_api(self, conversation: list[dict]) -> dict:
        """
        Send conversation to the language model’s API
        and return the reply. Should be overridden by subclasses.
        """
        return {"role": "assistant", "content": "Hello, as the base implementation of SLM, this is all I can say."}

    #
    # Helper functions for GPT-like completion models
    #
    @Logs.do_log_entry_and_exit()
    def _make_completion_prompt(self, conversation: list[dict]) -> str:
        system = {'role': 'system', 'content': Prompts.make_prompt(__name__, "completion")}
        return str([system] + conversation)

    def _parse_llm_response(self, response) -> dict:
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

        return parsed_data[0]

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
    @Utils.do_canonicalize_user_input_and_discuss_result('user_input')
    def do_discuss(self, user_input: list[dict], conversation: list[dict]) -> dict:
        """
        Pass through user input to the adapter and return the replies
        """
        return self.adapter.query_all(user_input, conversation)
