from openssm.core.ssm.abstract_ssm import AbstractSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.base_backend import BaseBackend


class BaseSSM(AbstractSSM):
    def __init__(self,
                 slm: AbstractSLM = None,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None):
        self.slm = slm or BaseSLM()
        self.slm.set_adapter(adapter or BaseAdapter())
        self.get_adapter().set_backends(backends or [BaseBackend()])

    def get_slm(self) -> AbstractSLM:
        """
        Return the previous assigned SLM,
        or a default SLM if none was assigned.
        """
        if self.slm is None:
            self.slm = BaseSLM()
        return self.slm

    def get_adapter(self) -> AbstractAdapter:
        """
        Return the previous assigned Adapter,
        or a default Adapter if none was assigned.
        """
        if self.get_slm().get_adapter() is None:
            self.get_slm().set_adapter(BaseAdapter())
        return self.get_slm().get_adapter()

    def get_backends(self) -> list[AbstractBackend]:
        """
        Return the previous assigned backends,
        or a default backend if none was assigned.
        """
        if self.get_adapter().get_backends() is None:
            self.get_adapter().set_backends([BaseBackend()])
        return self.get_adapter().get_backends()

    def discuss(self,
                conversation_id: str,
                user_input: list[dict]) -> list[dict]:
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

    def infer(self, input_facts: dict) -> list[str]:
        return self.get_adapter().infer(input_facts)

    def solve_problem(self, problem_description: list[str]) -> list[str]:
        pass

    def add_backend(self, backend: AbstractBackend):
        return self.get_adapter().add_backend(backend)
