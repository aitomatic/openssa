from abc import ABC, abstractmethod


# pylint disable=wduplicate-code
class ConversationDB(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def append_conversation(self, conversation_id, user_input):
        pass

    @abstractmethod
    def get_conversation(self, conversation_id):
        pass

    @abstractmethod
    def close(self):
        pass
