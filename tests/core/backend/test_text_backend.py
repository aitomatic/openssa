import unittest
from openssm.core.backend.text_backend import TextBackend
from openssm.core.inferencer.base_inferencer import BaseInferencer


class TestTextBackend(unittest.TestCase):

    def setUp(self):
        self.backend = TextBackend()

    def test_add_fact(self):
        self.backend.add_fact('fact1')
        self.assertIn('fact: fact1', self.backend.all_texts())

    def test_add_heuristic(self):
        self.backend.add_heuristic('heuristic1')
        self.assertIn('heuristic: heuristic1', self.backend.all_texts())

    def test_add_inferencer(self):
        inferencer = BaseInferencer()
        self.backend.add_inferencer(inferencer)
        self.assertIn(f'inferencer: {inferencer}', self.backend.all_texts())

    def test_query(self):
        self.backend.add_fact('fact1')
        self.backend.add_heuristic('heuristic1')
        inferencer = BaseInferencer()
        self.backend.add_inferencer(inferencer)

        expected_response = {'response': [
            'fact: fact1',
            'heuristic: heuristic1',
            f'inferencer: {inferencer}',
        ]}

        responses = self.backend.query('123', 'test')

        # Verify each response is in the expected responses
        for item in responses['response']:
            self.assertIn(item, expected_response['response'])
