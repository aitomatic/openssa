import unittest
from unittest.mock import MagicMock, patch
from openssm.integrations.openai.slm import ChatCompletionSLM, GPT3ChatCompletionSLM, CompletionSLM, GPT3CompletionSLM
from openssm.utils.config import Config


Config.OPENAI_API_URL = "test_url"
Config.OPENAI_API_KEY = "test_key"

# pylint: disable=protected-access

class TestChatCompletionSLM(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
    def test_call_lm_api(self, mock_create):
        fake_response = MagicMock()
        fake_response.choices[0].message = "Test Response"
        mock_create.return_value = fake_response
        slm = ChatCompletionSLM()
        conversation = [{'content': 'Test Content'}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response, "Test Response")


class TestCompletionSLM(unittest.TestCase):
    @patch('openai.Completion.create')
    def test_call_lm_api(self, mock_create):
        fake_response = MagicMock()
        fake_response.choices[0].text = "Test Response"
        mock_create.return_value = fake_response
        slm = CompletionSLM()
        conversation = [{'content': 'Test Content'}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response["content"], "Test Response")


class TestGPT3CompletionSLM(unittest.TestCase):
    def test_constructor_default_values(self):
        slm = GPT3CompletionSLM(api_key="test_key", api_base="test_api_base", adapter=None)
        self.assertEqual(slm.api_key, "test_key")
        self.assertEqual(slm.api_base, "test_api_base")
        self.assertEqual(slm.model, "text-davinci-002")

    @patch('openai.Completion.create')
    def test_call_lm_api(self, mock_create):
        fake_response = MagicMock()
        fake_response.choices[0].text = "Test Response"
        mock_create.return_value = fake_response
        slm = GPT3CompletionSLM()
        conversation = [{'content': 'Test Content'}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response["content"], "Test Response")


class TestGPT3ChatCompletionSLM(unittest.TestCase):
    def test_constructor_default_values(self):
        slm = GPT3ChatCompletionSLM(api_key="test_key", api_base="test_api_base", adapter=None)
        self.assertEqual(slm.api_key, "test_key")
        self.assertEqual(slm.api_base, "test_api_base")
        self.assertEqual(slm.model, "gpt-3.5-turbo")

    @patch('openai.ChatCompletion.create')
    def test_call_lm_api(self, mock_create):
        fake_response = MagicMock()
        fake_response.choices[0].message = "Test Response"
        mock_create.return_value = fake_response
        slm = GPT3ChatCompletionSLM()
        conversation = [{'content': 'Test Content'}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response, "Test Response")
