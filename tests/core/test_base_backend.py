from unittest.mock import Mock
from openssm.core.backend.base_backend import BaseBackend


def test_process():
    backend = BaseBackend()
    backend.process = Mock()
    backend.process("conversation_1", "Hello")
    backend.process.assert_called_with("conversation_1", "Hello")
