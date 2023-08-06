import unittest
from unittest.mock import Mock, patch
from openssm.core.ssm.rag_ssm import RAGSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.ssm.rag_ssm import AbstractRAGBackend


class TestRAGSSM(unittest.TestCase):
    def setUp(self):
        self.slm_mock = Mock(AbstractSLM)
        self.rag_backend_mock = Mock(AbstractRAGBackend)
        self.rag_ssm = RAGSSM(self.slm_mock, self.rag_backend_mock, "Test RAG SSM")

    def test_read_directory(self):
        self.rag_ssm.read_directory("test_dir", True)
        self.rag_backend_mock.read_directory.assert_called_with("test_dir", True)

    def test_read_gdrive(self):
        self.rag_ssm.read_gdrive("test_id", "test_dir", True)
        self.rag_backend_mock.read_gdrive.assert_called_with("test_id", "test_dir", True)

    def test_discuss(self):
        user_input = [{"role": "user", "content": "test content"}]
        rag_response = [{"role": "assistant", "content": "test response"}]
        self.slm_mock.discuss.return_value = rag_response
        # self.rag_backend_mock.discuss.return_value = rag_response
        self.rag_backend_mock.query.return_value = rag_response
        response = self.rag_ssm.discuss(user_input, "test_id")

        # Verify the SLM's discuss method was called with the combined user input and rag response
        self.slm_mock.discuss.assert_called()
        # Verify the returned response matches the mock SLM's response
        self.assertEqual(response, rag_response)

    @patch('openssm.core.ssm.rag_ssm.Prompts.get_module_prompt')
    def test__combine_inputs(self, get_module_prompt_mock):
        get_module_prompt_mock.return_value = "{user_input} {rag_response}"
        user_input = [{"role": "user", "content": "test content"}]
        rag_response = [{"role": "assistant", "content": "test response"}]
        expected_combined = [{"role": "user", "content": "test content test response"}]

        # pylint: disable=protected-access
        combined = self.rag_ssm._combine_inputs(user_input, rag_response)

        self.assertEqual(combined, expected_combined)
