from ..config import Config
from unittest.mock import Mock
from core.backend.base_backend import BaseBackend


config = Config()


def test_process():
    backend = BaseBackend()
    backend.process = Mock()
    backend.process("conversation_1", "Hello")
    backend.process.assert_called_with("conversation_1", "Hello")
