import os
import unittest
from unittest.mock import patch, Mock
from openssm.integrations.huggingface.slm import Falcon7bSLM, SLM as HuggingFaceBaseSLM
from openssm import Config


Config.FALCON7B_API_URL = os.environ["FALCON7B_API_URL"] = "test_url"
Config.FALCON7B_API_KEY = os.environ["FALCON7B_API_KEY"] = "test_key"

class TestHuggingFaceBaseSLM(unittest.TestCase):

    # Test for HuggingFaceBaseSLM in remote mode, where it calls a remote API
    @patch('openssm.integrations.huggingface.slm.request')
    def test_call_lm_api_remote_mode(self, mock_request):
        # Mocking a successful response from the remote API
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = '{"role": "assistant", "content": "Test response"}'
        mock_request.return_value = response_mock

        # Initializing the instance of HuggingFaceBaseSLM
        instance = HuggingFaceBaseSLM(model_name='test',
                                      model_url='http://test-url',
                                      model_server_token='test-token')

        # Simulating a call to the remote API and asserting the response
        # pylint: disable=protected-access
        result = instance._call_lm_api([{"role": "user", "content": "hello"}])
        self.assertEqual(result,
                         {"role": "assistant", "content": "Test response"})


class TestFalcon7bSLM(unittest.TestCase):

    # Test for initializing Falcon7bSLM
    @patch('openssm.integrations.huggingface.slm.SLM.__init__')
    def test_init(self, mock_super_init):
        # Initializing the instance of Falcon7bSLM
        instance = Falcon7bSLM()
        assert instance is not None

        # Asserting super's __init__ has been called with expected arguments
        mock_super_init.assert_called_once_with(
            model_name="tiiuae/falcon-7b",
            model_url=Config.FALCON7B_API_URL or "NONE",
            model_server_token=Config.FALCON7B_API_KEY or "value is not set",
            adapter=None)
