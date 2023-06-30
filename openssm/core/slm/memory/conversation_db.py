import abc

class ConversationDB(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def create_table(self):
        pass

    @abc.abstractmethod
    def append_conversation(self, conversation_id, user_input):
        pass

    @abc.abstractmethod
    def get_conversation(self, conversation_id):
        pass

    @abc.abstractmethod
    def close(self):
        pass
