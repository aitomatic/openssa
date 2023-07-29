from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.base_backend import BaseBackend


class TextBackend(BaseBackend):
    def __init__(self):
        super().__init__()
        self.texts = []

    # pylint: disable=unused-argument
    def query(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        responses = [{"response": text} for text in self.texts]
        return responses

    def all_texts(self):
        return self.texts

    def add_fact(self, fact: str):
        super().add_fact(fact)
        self.texts.append(f"fact: {fact}")

    def add_inferencer(self, inferencer: AbstractInferencer):
        super().add_inferencer(inferencer)
        self.texts.append(f"inferencer: {inferencer}")

    def add_heuristic(self, heuristic: str):
        super().add_heuristic(heuristic)
        self.texts.append(f"heuristic: {heuristic}")
