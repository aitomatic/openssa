from .base_ssm import BaseSSM
from openssm.core.slm.gpt3_slm import GPT3ChatCompletionSLM
from openssm.core.backend.abstract_backend import AbstractBackend


class GPT3LlamaIndexSSM(BaseSSM):
    def __init__(self, backends: list[AbstractBackend]):
        slm = GPT3ChatCompletionSLM()
        # adapter = LlamaIndexAdapter()
        adapter = None  # FIXME
        backends = None  # FIXME
        super().__init__(slm, adapter, backends)

    def process(self, conversation_id: str, user_input: str):
        # The SLM parses the user input and translates it
        # into one or more calls to the Adapter
        adapter_calls = self.slm.process(user_input)
        
        responses = []
        for call in adapter_calls:
            method = call['method']
            params = call['params']

            # The Adapter executes the method and
            # interacts with the appropriate Backend(s)
            if hasattr(self.adapter, method):
                result = getattr(self.adapter, method)(*params)
                responses.append(result)

        # The SLM then translates the Adapter responses
        # back into natural language
        output = self.slm.generate_output(responses)
        return output

    def add_backend(self, backend: AbstractBackend):
        self.backends.append(backend)

    def remove_backend(self, backend: AbstractBackend):
        self.backends.remove(backend)
