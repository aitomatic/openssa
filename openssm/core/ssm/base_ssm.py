from .abstract_ssm import AbstractSSM
from core.slm.abstract_slm import AbstractSLM
from core.adapter.abstract_adapter import AbstractAdapter
from core.backend.abstract_backend import AbstractBackend


class BaseSSM(AbstractSSM):
    def __init__(self,
                 slm: AbstractSLM = None,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        self.slm = slm
        if (slm is not None):
            slm.set_adapter(adapter)
        if (adapter is not None):
            adapter.set_backends(backends)

    def get_slm(self) -> AbstractSLM:
        return self.slm

    def get_adapter(self) -> AbstractAdapter:
        return None if self.get_slm() is None else self.get_slm().get_adapter()

    def get_backends(self) -> list[AbstractBackend]:
        if self.get_adapter() is None:
            return None
        else:
            self.get_adapter().get_backends()

    def discuss(self, conversation_id: str, user_input: str):
        return self.get_slm().discuss(conversation_id, user_input)

    def api_call(self, function_name, *args, **kwargs):
        return self.get_adapter().api_call(function_name, *args, **kwargs)

    def reset_memory(self):
        if self.get_slm() is not None:
            self.get_slm().reset_memory()

    def list_facts(self) -> list[str]:
        return self.get_adapter().list_facts()

    def list_inferencers(self) -> list[str]:
        return self.get_adapter().list_inferencers()

    def list_heuristics(self) -> list[str]:
        return self.get_adapter().list_heuristics()

    def select_facts(self, criteria: dict) -> list[str]:
        return self.get_adapter().select_facts(criteria)

    def select_inferencers(self, criteria: dict) -> list[str]:
        return self.get_adapter().select_inferencers(criteria)

    def select_heuristics(self, criteria: dict) -> list[str]:
        return self.get_adapter().select_heuristics(criteria)

    def infer(self, criteria: dict) -> list[str]:
        return self.get_adapter().infer(criteria)

    def solve_problem(self, problem_description: list[str]) -> list[str]:
        return super().solve_problem(problem_description)

    def add_backend(self, backend: AbstractBackend):
        return super().add_backend(backend)
