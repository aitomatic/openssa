import os
import unittest
from unittest.mock import MagicMock, patch
from openssa.integrations.openai.ssm import GPT3CompletionSLM, GPT3ChatCompletionSLM
from openssa.utils.config import Config

Config.OPENAI_API_URL = os.environ["OPENAI_API_URL"] = "test_url"
Config.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] = "test_key"
Config.OPENAI_ENGINE = os.environ["OPENAI_ENGINE"] = "test_engine"
Config.OPENAI_MODEL = os.environ["OPENAI_MODEL"] = "test_model"

# pylint: disable=protected-access


class TestGPT3CompletionSLM(unittest.TestCase):
    def test_constructor_default_values(self):
        slm = GPT3CompletionSLM()
        self.assertEqual(slm.api_context.key, "test_key")
        self.assertEqual(slm.api_context.base, "test_url")
        self.assertEqual(slm.api_context.model, "text-davinci-002")

    @patch('openai.resources.Completions.create')
    def do_not_test_call_lm_api(self, mock_create): #TODO fix this later
        fake_response = MagicMock()
        fake_response.choices[0].text = "Test Response"
        mock_create.return_value = fake_response
        slm = GPT3CompletionSLM()
        conversation = [{"content": "Test Content"}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response["content"], "Test Response")


class TestGPT3ChatCompletionSLM(unittest.TestCase):
    def test_constructor_default_values(self):
        slm = GPT3ChatCompletionSLM()
        self.assertEqual(slm.api_context.key, "test_key")
        self.assertEqual(slm.api_context.base, "test_url")
        self.assertEqual(slm.api_context.model, "gpt-3.5-turbo")

    @patch('openai.resources.chat.Completions.create')
    def test_call_lm_api(self, mock_create):
        fake_response = MagicMock()
        fake_response.choices[0].message.content = "Test Response"
        mock_create.return_value = fake_response
        slm = GPT3ChatCompletionSLM()
        conversation = [{"content": "Test Content"}]
        response = slm._call_lm_api(conversation)
        self.assertEqual(response, "Test Response")
