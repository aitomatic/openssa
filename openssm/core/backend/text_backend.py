from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.base_backend import BaseBackend


class TextBackend(BaseBackend):
    def __init__(self):
        super().__init__()
        self.texts = set()

    # pylint: disable=unused-argument
    def query(self, conversation_id: str, user_input: str) -> list({}):
        responses = [{"item": text} for text in self.texts]
        return responses

    def all_texts(self):
        return self.texts

    def add_fact(self, fact: str):
        super().add_fact(fact)
        self.texts.add(f"fact: {fact}")

    def add_inferencer(self, inferencer: AbstractInferencer):
        super().add_inferencer(inferencer)
        self.texts.add(f"inferencer: {inferencer}")

    def add_heuristic(self, heuristic: str):
        super().add_heuristic(heuristic)
        self.texts.add(f"heuristic: {heuristic}")

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
