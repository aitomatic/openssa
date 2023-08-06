from typing import Any
from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.utils.logs import Logs


class BaseBackend(AbstractBackend):
    def __init__(self):
        self._facts = set()
        self._inferencers = set()
        self._heuristics = set()

    # pylint: disable=unused-argument
    @Logs.do_log_entry_and_exit()
    def query(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        The base backend merely calls query2 and returns the first element of the tuple.
        """
        # pylint: disable=unused-variable
        response_dicts, response_object = self.query2(user_input, conversation_id)
        return response_dicts

    @Logs.do_log_entry_and_exit()
    def query2(self, user_input: list[dict], conversation_id: str = None) -> tuple[list[dict], Any]:
        """
        Query the index with the user input.

        Returns a tuple comprising (a) the response dicts and (b) the response object, if any.
        """
        return None, None

    def load_all(self):
        """
        The base backend does not load anything.
        It gets all its facts, inferencers, and heuristics
        through the add_* methods.
        """

    def add_fact(self, fact: str):
        self.facts.add(fact)

    def add_inferencer(self, inferencer: AbstractInferencer):
        self.inferencers.add(inferencer)

    def add_heuristic(self, heuristic: str):
        self.heuristics.add(heuristic)

    @property
    def facts(self):
        return self._facts

    @property
    def inferencers(self):
        return self._inferencers

    @property
    def heuristics(self):
        return self._heuristics

    def select_facts(self, criteria):
        """
        The base backend simply returns all facts.
        """
        assert criteria is not None
        return self.facts

    def select_inferencers(self, criteria):
        """
        The base backend simply returns all inferencers.
        """
        assert criteria is not None
        return self.inferencers

    def select_heuristics(self, criteria):
        """
        The base backend simply returns all heuristics.
        """
        assert criteria is not None
        return self.heuristics

    def save(self, storage_dir: str):
        """Saves to the specified directory."""
        pass

    def load(self, storage_dir: str):
        """Loads from the specified directory."""
        pass
