from .abstract_adapter import AbstractAdapter
from core.backend.abstract_backend import AbstractBackend


class BaseAdapter(AbstractAdapter):
    def __init__(self, backends: list = None):
        self.backends = backends or []

    def get_backends(self) -> list[AbstractBackend]:
        return self.backends

    def add_backend(self, backend: AbstractBackend):
        self.backends.append(backend)

    def set_backends(self, backends: list):
        self.backends = backends

    def list_facts(self):
        pass

    def list_inferencers(self):
        pass

    def list_heuristics(self):
        pass

    def select_facts(self, criteria):
        pass

    def select_inferencers(self, criteria):
        pass

    def select_heuristics(self, criteria):
        pass
