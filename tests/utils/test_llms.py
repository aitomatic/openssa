import unittest
from unittest.mock import Mock, patch
from openssa.utils.llms import AnLLM, BasicUsageLogger


class TestAnLLM(unittest.TestCase):
    def setUp(self):
        self.model = "test-model"
        self.api_base = "https://api.example.com"
        self.api_key = "testapikey"
        self.user_id = "testuser"
        self.usage_logger = Mock(spec=BasicUsageLogger)

    def test_initialization(self):
        anllm = AnLLM(
            self.model, self.api_base, self.api_key, self.user_id, self.usage_logger
        )
        self.assertEqual(anllm.model, self.model)
        self.assertEqual(anllm.api_base, self.api_base)
        self.assertEqual(anllm.api_key, self.api_key)
        self.assertEqual(anllm.user_id, self.user_id)
        self.assertIs(anllm.usage_logger, self.usage_logger)

    @patch("openssa.utils.llms.AnLLM.client")
    def test_call_is_chat_true(self, mock_client):
        # Setup
        anllm = AnLLM(self.model, usage_logger=self.usage_logger)
        mock_result = {"dummy": "result"}
        mock_client.chat.completions.create.return_value = mock_result

        # Action
        result = anllm.call(is_chat=True, test_arg="value")

        # Assert
        self.assertEqual(result, mock_result)
        self.usage_logger.log_usage.assert_called_once()


if __name__ == "__main__":
    unittest.main()
