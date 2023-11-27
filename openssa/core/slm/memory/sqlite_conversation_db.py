import sqlite3
from openssa.core.slm.memory.conversation_db import ConversationDB


class SQLiteConversationDB(ConversationDB):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conversation_db = None
        self.cursor = None

    def connect(self):
        self.conversation_db = sqlite3.connect(self.db_name)
        self.cursor = self.conversation_db.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations
                                (id text PRIMARY KEY, history text)''')
        self.conversation_db.commit()

    def append_conversation(self, conversation_id, user_input):
        self.cursor.execute(
            'SELECT * FROM conversations WHERE id=?',
            (conversation_id,))
        conversation = self.cursor.fetchone()
        if conversation is None:
            self.cursor.execute(
                "INSERT INTO conversations VALUES (?,?)",
                (conversation_id, user_input))
        else:
            updated_conversation = conversation[1] + "\n" + user_input
            self.cursor.execute(
                "UPDATE conversations SET history = ? WHERE id = ?",
                (updated_conversation, conversation_id))
        self.conversation_db.commit()

    def get_conversation(self, conversation_id):
        self.cursor.execute(
            "SELECT * FROM conversations WHERE id=?",
            (conversation_id,))
        conversation = self.cursor.fetchone()
        if conversation is not None:
            return conversation[1]
        return None

    def close(self):
        self.conversation_db.close()
