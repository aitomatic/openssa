import abc
import sqlite3
import ...config
import conversation_db

class SQLiteConversationDB(ConversationDB):
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self.conversation_db = sqlite3.connect(self.db_name)
        self.cursor = self.conversation_db.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations
                                (id text PRIMARY KEY, history text)''')
        self.conversation_db.commit()

    def append_conversation(self, conversation_id, user_input):
        self.cursor.execute('SELECT * FROM conversations WHERE id=?', (conversation_id,))
        conversation = self.cursor.fetchone()
        if conversation is None:
            self.cursor.execute("INSERT INTO conversations VALUES (?,?)", (conversation_id, user_input))
        else:
            updated_conversation = conversation[1] + "\n" + user_input
            self.cursor.execute("UPDATE conversations SET history = ? WHERE id = ?", (updated_conversation, conversation_id))
        self.conversation_db.commit()

    def get_conversation(self, conversation_id):
        self.cursor.execute('SELECT * FROM conversations WHERE id=?', (conversation_id,))
        conversation = self.cursor.fetchone()
        if conversation is not None:
            return conversation[1]
        return None

    def close(self):
        self.conversation_db.close()

class BaseNLUSLM(AbstractSLM, ABC):
    def __init__(self, adapter, config):
        super().__init__(adapter)
        self.db = SQLiteConversationDB(config.db_config)
        self.db.connect()
        self.db.create_table()

    def append_conversation(self, conversation_id, user_input):
        self.db.append_conversation(conversation_id, user_input)

    def get_conversation(self, conversation_id):
        return self.db.get_conversation(conversation_id)

    def process(self, conversation_id, user_input):
        self.append_conversation(conversation_id, user_input)
        return self.translate_to_adapter_calls(self.get_conversation(conversation_id))

    def close(self):
        self.db.close()
