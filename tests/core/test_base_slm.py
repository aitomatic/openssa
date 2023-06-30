from ..config import Config
from unittest.mock import Mock
from core.slm.base_slm import BaseSLM
from core.adapter.base_adapter import BaseAdapter


config = Config()


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
