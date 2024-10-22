"""
==============================================
[future work] Database Informational Resources
==============================================

This module contains `DbResource` class,
which enables querying information from relational databases.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .abstract import AbstractResource
from ._global import global_register


class MySQLDatabase:
    def __init__(self):
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.config = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME')
        }

    def create_engine(self):
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        return create_engine(connection_string)

    def get_session(self):
        return self.Session()


@global_register
@dataclass
class DbResource(AbstractResource):
    """Database Informational Resource."""
    query: str

    def __post_init__(self):
        """Post-initialize database resource."""
        self.db = MySQLDatabase()

    @property
    def unique_name(self) -> str:
        """Return globally-unique name of Resource."""
        return f"DBResource_{self.db.config['host']}_{self.db.config['database']}"

    @property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of Resource."""
        return f"Database at {self.db.config['host']}/{self.db.config['database']}"

    def fetch_data(self) -> list[tuple[Any]]:
        """Fetch data from the database using the provided query."""
        session = self.db.get_session()
        result = session.execute(text(self.query))
        return result.fetchall()

    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question from database-stored Informational Resource."""
        data = self.fetch_data()
        # Here you can implement a more sophisticated way to generate answers from the data
        # For simplicity, we will just return the fetched data as a string
        return str(data)

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        if hasattr(self, 'db'):
            self.db.Session.close_all()
