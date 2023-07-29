from typing import Callable
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.backend.text_backend import TextBackend
from openssm.core.inferencer.abstract_inferencer import AbstractInferencer


class BaseAdapter(AbstractAdapter):
    """Base adapter class for SSMs."""

    def __init__(self, backends: list[AbstractBackend] = None):
        self.backends = backends or []

    def query(self, user_input: str, conversation_id: str = None) -> list[dict]:
        """
        Queries the backends for a response to the user's input.
        :param user_query: The user's input.
        :return: The backend's response.
        """
        responses = [
            r for b in self.backends for r in b.query(
                user_input, conversation_id
            )]
        return responses

    def get_backends(self) -> list[AbstractBackend]:
        """
        Side effect: if no backends are set, a default TextBackend is created.
        """
        if self.backends is None or len(self.backends) == 0:
            self.backends = [TextBackend()]
        return self.backends

    def add_backend(self, backend: AbstractBackend):
        """
        Add a backend to the list of backends.
        """
        self.backends.append(backend)

    def set_backends(self, backends: list):
        """
        Set the list of backends.
        """
        self.backends = backends

    def enumerate_backends(self, lambda_function: Callable):
        """Enumerate backends and apply lambda function to each backend."""
        results = []
        for backend in self.backends:
            results.append(lambda_function(backend))

    def list_facts(self):
        """List facts from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.list_facts())

    def list_inferencers(self):
        """List inferencers from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.list_inferencers())

    def list_heuristics(self):
        """List heuristics from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.list_heuristics())

    def select_facts(self, criteria):
        """Select facts from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.select_facts(criteria))

    def select_inferencers(self, criteria):
        """Select inferencers from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.select_inferencers(criteria))

    def select_heuristics(self, criteria):
        """Select heuristics from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.select_heuristics(criteria))

    def _get_first_backend(self):
        """
        Get the first backend we have. If we currently have
        none, go ahead and add a default TextBackend.
        """
        return self.get_backends()[0]

    def add_fact(self, fact: str):
        """Idiom: add a fact to the first backend we have."""
        self._get_first_backend().add_fact(fact)

    def add_inferencer(self, inferencer: AbstractInferencer):
        self._get_first_backend().add_inferencer(inferencer)

    def add_heuristic(self, heuristic: str):
        self._get_first_backend().add_heuristic(heuristic)

    def persist(self, persist_dir: str):
        """Persists to the specified directory."""
        pass

    def load(self, persist_dir: str):
        """Loads from the specified directory."""
        pass
