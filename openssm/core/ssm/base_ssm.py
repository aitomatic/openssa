import os
import uuid
from openssm.core.ssm.abstract_ssm import AbstractSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.base_backend import BaseBackend
from openssm.utils.utils import Utils


class BaseSSM(AbstractSSM):
    def __init__(self,
                 slm: AbstractSLM = None,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None,
                 name: str = None):
        self._slm = slm
        self.slm.adapter = adapter
        self.adapter.backends = backends
        self._name = name

    @property
    def slm(self) -> AbstractSLM:
        """
        Return the previous assigned SLM,
        or a default SLM if none was assigned.
        """
        if self._slm is None:
            self._slm = BaseSLM()
        return self._slm

    @slm.setter
    def slm(self, slm: AbstractSLM):
        self._slm = slm

    @property
    def adapter(self) -> AbstractAdapter:
        """
        Return the previous assigned Adapter,
        or a default Adapter if none was assigned.
        """
        if self.slm.adapter is None:
            self.slm.adapter = BaseAdapter()
        return self.slm.adapter

    @adapter.setter
    def adapter(self, adapter: AbstractAdapter):
        self.slm.adapter = adapter

    @property
    def backends(self) -> list[AbstractBackend]:
        """
        Return the previous assigned backends,
        or a default backend if none was assigned.
        """
        if self.adapter.backends is None:
            self.adapter.backends = [BaseBackend()]
        return self.adapter.backends

    @backends.setter
    def backends(self, backends: list[AbstractBackend]):
        self.adapter.backends = backends

    @property
    def name(self) -> str:
        """
        Return the previous assigned name,
        or a default name if none was assigned.
        """
        if self._name is None:
            self._name = f"ssm-{uuid.uuid4().hex[:8]}"
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @Utils.do_canonicalize_user_input_and_query_response('user_input')
    def discuss(self, user_input: list[dict], conversation_id: str = None) -> list[dict]:
        return self.slm.discuss(user_input, conversation_id)

    def api_call(self, function_name, *args, **kwargs):
        return self.adapter.api_call(function_name, *args, **kwargs)

    def reset_memory(self):
        if self.slm is not None:
            self.slm.reset_memory()

    @property
    def facts(self) -> list[str]:
        """
        Return the facts from the adapter.
        """
        return self.adapter.facts

    @property
    def inferencers(self) -> list[str]:
        """
        Return the inferencers from the adapter.
        """
        return self.adapter.inferencers

    @property
    def heuristics(self) -> list[str]:
        """
        Return the heuristics from the adapter.
        """
        return self.adapter.heuristics

    def select_facts(self, criteria: dict) -> list[str]:
        return self.adapter.select_facts(criteria)

    def select_inferencers(self, criteria: dict) -> list[str]:
        return self.adapter.select_inferencers(criteria)

    def select_heuristics(self, criteria: dict) -> list[str]:
        return self.adapter.select_heuristics(criteria)

    def infer(self, input_facts: dict) -> list[str]:
        return self.adapter.infer(input_facts)

    def solve_problem(self, problem_description: list[str]) -> list[str]:
        pass

    def add_knowledge(self, knowledge_source_uri: str, knowledge_type=None):
        """Uploads a knowledge source (documents, text, files, etc.)"""
        # self.adapter.add_knowledge(knowledge_source_uri, knowledge_type)

    @property
    def _default_storage_dir(self) -> str:
        base_dir = os.environ.get("OPENSSM_STORAGE_DIR", ".openssm")
        return os.path.join(base_dir, self.name)

    def save(self, storage_dir: str = None):
        """Saves the SSM to the specified directory."""
        storage_dir = storage_dir or self._default_storage_dir
        self.slm.save(storage_dir)
        self.adapter.save(storage_dir)
        self.adapter.enumerate_backends(lambda backend: backend.save(storage_dir))

    def load(self, storage_dir: str = None):
        """Loads the SSM from the specified directory."""
        storage_dir = storage_dir or self._default_storage_dir
        self.slm.load(storage_dir)
        self.adapter.load(storage_dir)
        self.adapter.enumerate_backends(lambda backend: backend.load(storage_dir))
