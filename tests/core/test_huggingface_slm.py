import unittest
from unittest.mock import patch, Mock
from openssm.core.slm.huggingface_slm import HuggingFaceBaseSLM
from openssm.core.slm.huggingface_slm import Falcon7bSLM, Falcon7bSLMLocal


class TestHuggingFaceBaseSLM(unittest.TestCase):

    # Test for HuggingFaceBaseSLM in local mode—the model is loaded locally
    @patch('openssm.core.slm.huggingface_slm.AutoTokenizer')
    @patch('openssm.core.slm.huggingface_slm.AutoModelForCausalLM')
    @patch('openssm.core.slm.huggingface_slm.pipeline')
    def test_init_local_mode(self, mock_pipeline, mock_model, mock_tokenizer):
        # Mocking the return values of the external dependencies
        mock_tokenizer.from_pretrained.return_value = Mock()
        mock_model.from_pretrained.return_value = Mock()
        mock_pipeline.return_value = Mock()

        # Initializing the instance of HuggingFaceBaseSLM
        instance = HuggingFaceBaseSLM(model_name='test')

        # Asserting if local_mode is True when the model_url is not provided
        self.assertEqual(instance.local_mode, True)

    # Test for HuggingFaceBaseSLM in remote mode, where it calls a remote API
    @patch('openssm.core.slm.huggingface_slm.request')
    def test_call_lm_api_remote_mode(self, mock_request):
        # Mocking a successful response from the remote API
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.text = "{'generated_text': 'Test response'}"
        mock_request.return_value = response_mock

        # Initializing the instance of HuggingFaceBaseSLM
        instance = HuggingFaceBaseSLM(model_name='test',
                                      model_url='http://test-url',
                                      model_server_token='test-token')

        # Asserting if local_mode is False when the model_url is provided
        self.assertEqual(instance.local_mode, False)

        # Simulating a call to the remote API and asserting the response
        result = instance.call_lm_api([{"role": "user", "content": "hello"}])
        self.assertEqual(result,
                         [{"role": "assistant", "content": "Test response"}])


class TestFalcon7bSLM(unittest.TestCase):

    # Test for initializing Falcon7bSLM
    @patch('openssm.core.slm.huggingface_slm.HuggingFaceBaseSLM.__init__')
    def test_init(self, mock_super_init):
        # Initializing the instance of Falcon7bSLM
        instance = Falcon7bSLM()
        assert instance is not None

        # Asserting super's __init__ has been called with expected arguments
        mock_super_init.assert_called_once_with(model_name="tiiuae/falcon-7b",
                                                model_url=None,
                                                model_server_token=None,
                                                adapter=None)


class TestFalcon7bSLMLocal(unittest.TestCase):

    # Test for initializing Falcon7bSLMLocal
    @patch('openssm.core.slm.huggingface_slm.HuggingFaceBaseSLM.__init__')
    def test_init(self, mock_super_init):
        # Initializing the instance of Falcon7bSLMLocal
        instance = Falcon7bSLMLocal()
        assert instance is not None

        # Asserting if super's __init__ has been called with expected arguments
        mock_super_init.assert_called_once_with(model_name="tiiuae/falcon-7b",
                                                model_url=None,
                                                model_server_token=None,
                                                adapter=None)
