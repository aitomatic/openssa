from .abstract_adapter import AbstractAdapter
from ..backend.abstract_backend import AbstractBackend


class BaseAdapter(AbstractAdapter):
    """Base adapter class for SSMs."""

    def __init__(self, backends: list = None):
        self.backends = backends or []

    def get_backends(self) -> list[AbstractBackend]:
        return self.backends

    def add_backend(self, backend: AbstractBackend):
        """"""
        self.backends.append(backend)

    def set_backends(self, backends: list):
        """"""
        self.backends = backends

    def enumerate_backends(self, lambda_function):
        """Enumerate backends and apply lambda function to each backend."""
        results = []
        for backend in self.backends:
            results.extend(lambda_function(backend))
        return results

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
