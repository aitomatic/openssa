from typing import Callable
from openssa.core.adapter.abstract_adapter import AbstractAdapter
from openssa.core.backend.abstract_backend import AbstractBackend
from openssa.core.backend.text_backend import TextBackend
from openssa.core.inferencer.abstract_inferencer import AbstractInferencer


class BaseAdapter(AbstractAdapter):
    """Base adapter class for SSMs."""

    def __init__(self, backends: list[AbstractBackend] = None):
        self._backends = backends

    # pylint: disable=too-many-branches
    # flake8: noqa: C901
    def query_all(self, user_input: str, conversation: list[dict] = None) -> list[dict]:
        """
        Queries the backends for a response to the user's input.
        :param user_query: The user's input.
        :return: The backend's responses
        """
        responses = []
        response_objects = []
        for b in self.backends:
            if b is not None:
                response = b.query(user_input, conversation)
                if isinstance(response, str):
                    responses.extend(response)

                elif isinstance(response, dict):
                    if "response" in response:
                        responses.extend(response["response"])
                    if "response_object" in response:
                        response_objects.extend(response["response_object"])

        if len(responses) == 0:
            return {"response": None, "response_object": None}

        if len(responses) == 1:
            if isinstance(response[0], str):
                if len(response_objects) == 0:
                    return {"response": responses[0]}
                if len(response_objects) == 1:
                    return {"response": responses[0], "response_object": response_objects[0]}
                return {"response": responses[0], "response_object": response_objects}

        return {"response": responses, "response_object": response_objects}

    @property
    def backends(self) -> list[AbstractBackend]:
        """
        Side effect: if no backends are set, a default TextBackend is created.
        """
        if self._backends is None or len(self._backends) == 0:
            self._backends = [TextBackend()]
        return self._backends

    def add_backend(self, backend: AbstractBackend):
        """
        Add a backend to the list of backends.
        """
        self.backends.append(backend)

    @backends.setter
    def backends(self, backends: list):
        """
        Set the list of backends.
        """
        self._backends = backends

    def enumerate_backends(self, lambda_function: Callable):
        """Enumerate backends and apply lambda function to each backend."""
        results = []
        for backend in self.backends:
            results.append(lambda_function(backend))

    @property
    def facts(self):
        """List facts from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.list_facts())

    @property
    def inferencers(self):
        """List inferencers from all backends."""
        return self.enumerate_backends(
            lambda backend: backend.list_inferencers())

    @property
    def heuristics(self):
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
        return self.backends[0]

    def add_fact(self, fact: str):
        """Idiom: add a fact to the first backend we have."""
        self._get_first_backend().add_fact(fact)

    def add_inferencer(self, inferencer: AbstractInferencer):
        self._get_first_backend().add_inferencer(inferencer)

    def add_heuristic(self, heuristic: str):
        self._get_first_backend().add_heuristic(heuristic)

    def save(self, storage_dir: str):
        """Saves to the specified directory."""
        pass

    def load(self, storage_dir: str):
        """Loads from the specified directory."""
        pass
