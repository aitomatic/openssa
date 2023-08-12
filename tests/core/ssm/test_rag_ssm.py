import unittest
from unittest.mock import MagicMock
from openssm.core.ssm.rag_ssm import RAGSSM
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.core.prompts import Prompts


# os.environ['OPENAI_API_URL'] = "test_url"
# os.environ['OPENAI_API_KEY'] = "test_key"
# Config.OPENAI_API_URL = "test_url"
# Config.OPENAI_API_KEY = "test_key"

class TestRAGSSM(unittest.TestCase):
    def test_initialization(self):
        slm = MagicMock()
        rag_backend = MagicMock()
        name = "TestName"
        storage_dir = "TestDirectory"

        rag_ssm = RAGSSM(slm=slm, rag_backend=rag_backend, name=name, storage_dir=storage_dir)

        # pylint: disable=protected-access
        self.assertEqual(rag_ssm._rag_backend, rag_backend)
        self.assertEqual(rag_ssm.slm, slm)

    def test_is_passthrough(self):
        rag_ssm = RAGSSM()
        self.assertTrue(rag_ssm.is_passthrough())

    def test_rag_backend_property(self):
        rag_backend = MagicMock()
        rag_ssm = RAGSSM(rag_backend=rag_backend)
        self.assertEqual(rag_ssm.rag_backend, rag_backend)

    def test_read_directory(self):
        rag_backend = MagicMock()
        storage_dir = "TestDirectory"
        rag_ssm = RAGSSM(rag_backend=rag_backend)
        rag_ssm.read_directory(storage_dir)
        rag_backend.read_directory.assert_called_with(storage_dir, False)

    def test_read_gdrive(self):
        rag_backend = MagicMock()
        folder_id = "TestFolder"
        storage_dir = "TestDirectory"
        rag_ssm = RAGSSM(rag_backend=rag_backend)
        rag_ssm.read_gdrive(folder_id, storage_dir)
        rag_backend.read_gdrive.assert_called_with(folder_id, storage_dir, False)

    def test_read_website(self):
        rag_backend = MagicMock()
        urls = ["http://example.com"]
        storage_dir = "TestDirectory"
        rag_ssm = RAGSSM(rag_backend=rag_backend)
        rag_ssm.read_website(urls, storage_dir)
        rag_backend.read_website.assert_called_with(urls, storage_dir, False)

    # Test for _make_conversation
    def test_make_conversation(self):
        rag_ssm = RAGSSM()
        user_input = [{'role': 'user', 'content': 'What is the capital of Spain?'}]
        rag_response = {'response': 'Madrid is the capital of Spain.'}

        system_instructions = Prompts.get_prompt(
            "openssm.core.ssm.rag_ssm", "_make_conversation", "system")

        combined_user_input = Prompts.get_prompt(
            "openssm.core.ssm.rag_ssm", "_make_conversation", "user"
        ).format(
            user_input=str(user_input[0]["content"]),
            rag_response=str(rag_response["response"]))

        expected_result = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": combined_user_input},
        ]
        # pylint: disable=protected-access
        result = rag_ssm._make_conversation(user_input, rag_response)
        self.assertEqual(result, expected_result)

    # Test for _sanitize_rag_response
    def test_sanitize_rag_response(self):
        rag_ssm = RAGSSM()
        response = [{"role": "assistant", "content": [{'role': 'assistant', 'content': 'Answer'}]}]
        expected_result = {"role": "assistant", "content": "Answer"}
        # pylint: disable=protected-access
        result = rag_ssm._sanitize_rag_response(response)
        self.assertEqual(result, expected_result)

    # Test for custom_discuss
    def test_custom_discuss(self):
        # Create a RAGSSM object
        rag_ssm = RAGSSM()

        # Set up user_input and conversation
        user_input = [{"role": "user", "content": "Question"}]
        conversation = [{"role": "system", "content": "Instructions"}]

        # Mock the RAG backend with a return value
        rag_response = {"response": "Madrid is the capital of Spain."}
        rag_backend_mock = MagicMock()
        rag_backend_mock.query.return_value = rag_response
        # pylint: disable=protected-access
        rag_ssm._rag_backend = rag_backend_mock

        # Mock the SLM
        slm_response = {"role": "assistant", "content": "Answer from SLM"}
        slm_mock = MagicMock()
        slm_mock.do_discuss.return_value = slm_response
        rag_ssm.slm = slm_mock

        # Test with a passthrough SLM
        rag_ssm.slm = PassthroughSLM()
        result = rag_ssm.custom_discuss(user_input, conversation)
        self.assertEqual(result, {"role": "assistant", "content": rag_response["response"]})

        # Test without RAG response
        rag_ssm.slm = slm_mock
        rag_backend_mock.query.return_value = None
        result = rag_ssm.custom_discuss(user_input, conversation)
        self.assertEqual(result, slm_response)

        # Test with both RAG response and SLM response
        # rag_backend_mock.query.return_value = rag_response
        # combined_input = "<combined input>"  # Define a proper value based on your implementation
        # slm_mock.do_discuss.side_effect = [slm_response, "final response"]
        # result = rag_ssm.custom_discuss(user_input, conversation)
        # self.assertEqual(result, "final response")
