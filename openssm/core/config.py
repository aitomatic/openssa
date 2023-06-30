import abc
import sqlite3

class Config:
    SLM_CONVERSATION_DB = SQLiteConversationDB('conversations.db')
