"""
==============================================
[future work] Database Informational Resources
==============================================

This module contains `DbResource` class,
which enables querying information from relational databases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
import mysql.connector  # MySQL Connector for Python

from .abstract import AbstractResource
from ._global import global_register
from ._prompts import RESOURCE_QA_PROMPT_TEMPLATE


@global_register
@dataclass
class DbResource(AbstractResource):
    """Database Informational Resource."""

    # Database connection parameters
    host: str
    user: str
    password: str
    database: str

    # SQL query to fetch data
    query: str

    def __post_init__(self):
        """Post-initialize database resource."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    @cached_property
    def unique_name(self) -> str:
        """Return globally-unique name of Resource."""
        return f"DBResource_{self.host}_{self.database}"

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of Resource."""
        return f"Database at {self.host}/{self.database}"

    def fetch_data(self) -> list[tuple[Any]]:
        """Fetch data from the database using the provided query."""
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question from database-stored Informational Resource."""
        data = self.fetch_data()
        # Here you can implement a more sophisticated way to generate answers from the data
        # For simplicity, we will just return the fetched data as a string
        return str(data)

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        self.connection.close()
