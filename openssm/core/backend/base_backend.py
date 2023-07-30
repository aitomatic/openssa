from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.abstract_backend import AbstractBackend


class BaseBackend(AbstractBackend):
    def __init__(self):
        self.facts = set()
        self.inferencers = set()
        self.heuristics = set()

    # pylint: disable=unused-argument
    def query(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        """
        The base backend does not query anything.
        Subclasses should query the backend with the user input,
        and return a tuple of (a) the response string, and
        (b) the more informative response object, if any.
        """
        return None

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

    def list_facts(self):
        return self.facts

    def list_inferencers(self):
        return self.inferencers

    def list_heuristics(self):
        return self.heuristics

    def select_facts(self, criteria):
        """
        The base backend simply returns all facts.
        """
        assert criteria is not None
        return self.list_facts()

    def select_inferencers(self, criteria):
        """
        The base backend simply returns all inferencers.
        """
        assert criteria is not None
        return self.list_inferencers()

    def select_heuristics(self, criteria):
        """
        The base backend simply returns all heuristics.
        """
        assert criteria is not None
        return self.list_heuristics()

    def persist(self, persist_dir: str):
        """Persists to the specified directory."""
        pass

    def load(self, persist_dir: str):
        """Loads from the specified directory."""
        pass
