import unittest
from unittest.mock import Mock
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.adapter.base_adapter import BaseAdapter
from openssm.core.slm.base_slm import PassthroughSLM


class MockAdapter(BaseAdapter):
    # since we don't call any methods from BaseAdapter, we don't need
    # to define any in our mock
    pass


def test_adapter():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    assert slm.adapter == adapter


def test_set_adapter():
    adapter1 = MockAdapter()
    adapter2 = MockAdapter()
    slm = BaseSLM(adapter1)
    slm.adapter = adapter2
    assert slm.adapter == adapter2


def test_discuss():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    # Replace discuss with a Mock object to track if it gets called
    slm.do_discuss = Mock()
    slm.do_discuss("conversation_1", "Hello")
    # Check that discuss was called with the correct parameters
    slm.do_discuss.assert_called_with("conversation_1", "Hello")


def test_reset_memory():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    # We replace reset_memory with a Mock object to track if it gets called
    slm.reset_memory = Mock()
    slm.reset_memory()
    slm.reset_memory.assert_called()  # Check that reset_memory was called


def test_llm_valid_response():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    response = ', {"role": "assistant", "content": "Message 1"}, invalid_response, {"role": "user", "content": "Message 2"}'

    expected_result = [
        {'role': 'assistant', 'content': 'Message 1'},
        {'role': 'user', 'content': 'Message 2'}
    ]

    # pylint: disable=protected-access
    parsed_data = slm._parse_llm_response(response)
    assert parsed_data == expected_result[0]


def _string_response(response):
    return {'role': 'assistant', 'content': response}


def test_llm_no_valid_json():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    response = ', invalid_response, random_string2'

    expected_result = _string_response(response)

    # pylint: disable=protected-access
    parsed_data = slm._parse_llm_response(response)
    assert parsed_data == expected_result


def test_llm_empty_response():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    response = ''

    expected_result = _string_response(response)

    # pylint: disable=protected-access
    parsed_data = slm._parse_llm_response(response)
    assert parsed_data == expected_result


class TestPassthroughSLM(unittest.TestCase):

    def setUp(self):
        # Mocking the adapter's query method
        self.mocked_adapter = Mock()
        self.mocked_adapter.query_all.return_value = {"response": "mock_response"}

        # Creating an instance of PassthroughSLM with the mocked adapter
        self.slm = PassthroughSLM()
        self.slm.adapter = self.mocked_adapter

    def test_discuss(self):
        user_input = [{"query": "test_query"}]
        conversation_id = "12345"
        response = self.slm.do_discuss(user_input, conversation_id)

        # Check if the response is correct
        self.assertEqual(response, {'role': 'assistant', 'content': 'mock_response'})
