from openssa.core.inferencer.abstract_inferencer import AbstractInferencer
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.utils.logs import Logs


class BaseBackend(AbstractBackend):
    def __init__(self):
        self._facts = set()
        self._inferencers = set()
        self._heuristics = set()

    # pylint: disable=unused-argument
    @Logs.do_log_entry_and_exit()
    def query(self, user_input: list[dict], conversation: list[dict] = None) -> dict:
        """
        Backends are expected to return a dict with the following keys:
        - response: a string
        - response_object: an object that has a lot more information about the response
        """
        return {"response": None, "response_object": None}

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
