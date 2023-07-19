from unittest.mock import Mock
from openssm.core.slm.base_slm import BaseSLM
from openssm.core.adapter.base_adapter import BaseAdapter


class MockAdapter(BaseAdapter):
    # since we don't call any methods from BaseAdapter, we don't need
    # to define any in our mock
    pass


def test_get_adapter():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    assert slm.get_adapter() == adapter


def test_set_adapter():
    adapter1 = MockAdapter()
    adapter2 = MockAdapter()
    slm = BaseSLM(adapter1)
    slm.set_adapter(adapter2)
    assert slm.get_adapter() == adapter2


def test_discuss():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    # Replace discuss with a Mock object to track if it gets called
    slm.discuss = Mock()
    slm.discuss("conversation_1", "Hello")
    # Check that discuss was called with the correct parameters
    slm.discuss.assert_called_with("conversation_1", "Hello")


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
    assert parsed_data == expected_result


def _string_response(response):
    return [{'assistant': response}]


def test_llm_no_valid_json():
    adapter = MockAdapter()
    slm = BaseSLM(adapter)
    response = ', invalid_response, random_string'

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
