from .abstract_backend import AbstractBackend


class BaseBackend(AbstractBackend):
    def __init__(self):
        pass

    def process(self, conversation_id: str, user_input: str):
        pass
