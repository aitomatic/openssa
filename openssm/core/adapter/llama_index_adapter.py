from dataclasses import dataclass
from typing import Any
from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class LlamaIndexAdapter(BaseAdapter):
    """
    The LlamaIndexAdapter is a concrete implementation of the AbstractAdapter
    that uses LlamaIndex.
    """

    @dataclass
    class _LlamaIndex:
        index: BaseIndex = None
        query_engine: BaseQueryEngine = None

    def __init__(self, backends: list[AbstractBackend] = None):
        """Initializes the LlamaIndexAdapter with a specific LlamaIndex."""
        super().__init__(backends)
        self._llama_indexes = [LlamaIndexAdapter._LlamaIndex]

    def _get_llama_indexes(self) -> list[_LlamaIndex]:
        if self._llama_indexes is None:
            self._llama_indexes = [LlamaIndexAdapter._LlamaIndex]
        return self._llama_indexes

    def _get_indexes(self) -> list[BaseIndex]:
        indexes = [lt.index for lt in self._get_llama_indexes()]
        return indexes

    def _get_query_engines(self) -> list[BaseQueryEngine]:
        query_engines = [lt.query_engine for lt in self._get_llama_indexes()]
        return query_engines

    def _query_llama(self, query: str) -> list[Any]:
        responses = []
        # pylint: disable=invalid-name
        for qe in self._get_query_engines():
            response = qe.query(query)
            responses.append(response)
        return responses

    def add_backend(self, backend: AbstractBackend):
        """
        Add a backend to the list of backends.
        Also connect it appropriately to the LlamaIndex.
        """
        super().add_backend(backend)
        self.backends.append(backend)

    def list_facts(self):
        """Lists all known facts."""
        # Query the index for documents classified as facts
        return self._query_llama("list all facts")

    def list_inferencers(self):
        """Lists all known inferencers."""
        # Query the index for documents classified as inferencers
        return self._query_llama("list all inferencers")

    def list_heuristics(self):
        """Lists all known heuristics."""
        # Query the index for documents classified as heuristics
        return self._query_llama("list all heuristics")

    def select_facts(self, criteria):
        """Selects or searches for facts based on provided criteria."""
        # Query the index for facts matching the criteria
        return self._query_llama(
            f"list all facts matching criteria: {criteria}")

    def select_inferencers(self, criteria):
        """Selects or searches for inferencers based on provided criteria."""
        # Query the index for inferencers matching the criteria
        return self._query_llama(
            f"list all inferencers matching criteria: {criteria}")

    def select_heuristics(self, criteria):
        """Selects or searches for heuristics based on provided criteria."""
        # Query the index for heuristics matching the criteria
        return self._query_llama(
            f"list all heuristics matching criteria: {criteria}")

    def infer(self, input_facts):
        """Makes inferences based on the provided input facts."""
        # Query the index and retrieve relevant inferencers
        results = self._query_llama((
            f"infer an appropriate conclusion"
            f" from the following inputs:{input_facts}"))
        # This is a simple example and may need to be enhanced
        # based on how the inference process should work
        return results

    def solve_problem(self, problem_description):
        """Solves a problem based on the provided description."""
        # Use the problem description to query index
        # and retrieve relevant heuristics
        results = self._query_llama(
            f"problem:{problem_description}")
        # This is a simple example and may need to be enhanced
        # based on how the problem-solving process should work
        return results
