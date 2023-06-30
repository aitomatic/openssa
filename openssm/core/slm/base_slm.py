from .abstract_slm import AbstractSLM
from core.adapter.abstract_adapter import AbstractAdapter


class BaseSLM(AbstractSLM):
    def __init__(self, adapter: AbstractAdapter = None):
        self.adapter = adapter

    def get_adapter(self) -> AbstractAdapter:
        return self.adapter

    def set_adapter(self, adapter: AbstractAdapter):
        self.adapter = adapter

    def discuss(self, conversation_id: str, user_input: str):
        pass

    def reset_memory(self):
        pass
