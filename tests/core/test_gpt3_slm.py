import pytest
from unittest.mock import patch, MagicMock
from openssm.core.slm.gpt3_slm import GPT3ChatCompletionSLM


@pytest.fixture(autouse=True)
def setup_class():
    # Mock the response from the chat/completion method
    pytest.mock_response = MagicMock()
    pytest.mock_message = {'role': 'assistant', 'content': 'Test response'}
    pytest.mock_response.choices = [MagicMock(message=pytest.mock_message)]
    # pytest.mock_func.return_value = pytest.mock_response
    pytest.user_input = [{'role': 'user', 'content': 'Test input'}]
    pytest.conversation_id = '123'


@patch('openai.ChatCompletion.create')
@patch('config.Config', new=MagicMock(OPENAI_API_KEY='test_key'))
def test_gpt3_chat_completion_discuss(mock_func):
    slm = GPT3ChatCompletionSLM()
    replies = slm.discuss(pytest.conversation_id, pytest.user_input)

    mock_func.return_value = pytest.mock_response

    # Assert that the create method was called with the expected arguments
    expected_messages = slm.conversations.get(pytest.conversation_id, [])
    mock_func.assert_called_once_with(
        model='gpt-3.5-turbo',
        messages=expected_messages,
        temperature=0.7
    )

    # Assert that the response is as expected
    assert replies == [expected_messages[1]]


@patch('openai.ChatCompletion.create')
def do_not_test_discuss(mock_create):
    # Mock the response from OpenAI API
    # mock_create.return_value = MagicMock()
    # choices=[MagicMock(text=" Test response")])

    conversation = [{'role': 'user', 'content': 'Test input'}]

    response = pytest.gpt3slm.discuss(
        'test_conversation_id',
        conversation
    )

    # Assert that the method was called with correct arguments
    mock_create.assert_called_with(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
    )

    # Assert the response is as expected
    print(response)
    # assert response == 'Test response'


def d_test_reset_memory():
    pytest.gpt3slm.conversations = {
        'test_conversation': ['Test input', 'Test response']
    }
    pytest.gpt3slm.reset_memory()
    assert pytest.gpt3slm.conversations == {}
