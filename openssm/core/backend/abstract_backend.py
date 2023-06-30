from abc import ABC, abstractmethod


class AbstractBackend(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, conversation_id: str, user_input: str):
        pass
