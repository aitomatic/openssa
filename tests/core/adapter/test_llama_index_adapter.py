import unittest
from unittest.mock import Mock, patch
from openssm.core.adapter.llama_index_adapter import LlamaIndexAdapter
from openssm.core.backend.abstract_backend import AbstractBackend


class TestLlamaIndexAdapter(unittest.TestCase):

    def setUp(self):
        self.base_index = Mock()
        self.query_engine = Mock()
        self.backend = Mock(spec=AbstractBackend)

        with patch.object(LlamaIndexAdapter, '_LlamaIndex') as self.mock_llama_index:
            self.mock_llama_index.index = self.base_index
            self.mock_llama_index.query_engine = self.query_engine
            self.adapter = LlamaIndexAdapter()

    def test_get_llama_indexes(self):
        # pylint: disable=protected-access
        indexes = self.adapter._get_llama_indexes()
        self.assertEqual(indexes, [self.mock_llama_index])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['fact1', 'fact2'])
    def test_list_facts(self, mock_query_llama):
        facts = self.adapter.list_facts()
        mock_query_llama.assert_called_once_with("list all facts")
        self.assertEqual(facts, ['fact1', 'fact2'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['inferencer1', 'inferencer2'])
    def test_list_inferencers(self, mock_query_llama):
        inferencers = self.adapter.list_inferencers()
        mock_query_llama.assert_called_once_with("list all inferencers")
        self.assertEqual(inferencers, ['inferencer1', 'inferencer2'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['heuristic1', 'heuristic2'])
    def test_list_heuristics(self, mock_query_llama):
        heuristics = self.adapter.list_heuristics()
        mock_query_llama.assert_called_once_with("list all heuristics")
        self.assertEqual(heuristics, ['heuristic1', 'heuristic2'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['fact1'])
    def test_select_facts(self, mock_query_llama):
        criteria = "criteria"
        facts = self.adapter.select_facts(criteria)
        mock_query_llama.assert_called_once_with(f"list all facts matching criteria: {criteria}")
        self.assertEqual(facts, ['fact1'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['inferencer1'])
    def test_select_inferencers(self, mock_query_llama):
        criteria = "criteria"
        inferencers = self.adapter.select_inferencers(criteria)
        mock_query_llama.assert_called_once_with(f"list all inferencers matching criteria: {criteria}")
        self.assertEqual(inferencers, ['inferencer1'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['heuristic1'])
    def test_select_heuristics(self, mock_query_llama):
        criteria = "criteria"
        heuristics = self.adapter.select_heuristics(criteria)
        mock_query_llama.assert_called_once_with(f"list all heuristics matching criteria: {criteria}")
        self.assertEqual(heuristics, ['heuristic1'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['inference'])
    def test_infer(self, mock_query_llama):
        input_facts = "input facts"
        inferences = self.adapter.infer(input_facts)
        mock_query_llama.assert_called_once_with(f"infer an appropriate conclusion from the following inputs:{input_facts}")
        self.assertEqual(inferences, ['inference'])

    @patch.object(LlamaIndexAdapter, '_query_llama', return_value=['problem solution'])
    def test_solve_problem(self, mock_query_llama):
        problem_description = "problem description"
        solutions = self.adapter.solve_problem(problem_description)
        mock_query_llama.assert_called_once_with(f"problem:{problem_description}")
        self.assertEqual(solutions, ['problem solution'])

    def test_add_backend(self):
        self.adapter.add_backend(self.backend)
        self.assertIn(self.backend, self.adapter.backends)
