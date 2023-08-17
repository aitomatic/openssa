import unittest
from unittest.mock import MagicMock, patch
from llama_index import Response
from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.llama_index.ssm import SSM as LlamaIndexSSM  # , GPT3SSM


class TestSSMClasses(unittest.TestCase):
    def test_llama_index_ssm(self):
        slm = MagicMock(spec=AbstractSLM)
        ssm = LlamaIndexSSM(slm)

        self.assertIsInstance(ssm.rag_backend, LlamaIndexBackend)

        with patch.object(ssm.rag_backend, 'read_directory') as mock_read_dir:
            ssm.read_directory("test_directory")
            mock_read_dir.assert_called_once_with("test_directory", False)

    def test_llama_index_ssm2(self):
        ssm = LlamaIndexSSM(PassthroughSLM())

        self.assertIsInstance(ssm.rag_backend, LlamaIndexBackend)
        self.assertIsInstance(ssm.slm, PassthroughSLM)

    def test_gpt3_llama_index_ssm(self):
        # ssm = GPT3SSM()
        # self.assertIsInstance(ssm.slm, GPT3ChatCompletionSLM)
        pass

class TestBackend(unittest.TestCase):
    def test_query_engine(self):
        backend = LlamaIndexBackend()
        backend.index = MagicMock(spec=BaseIndex)
        backend.index.as_query_engine = MagicMock(return_value=MagicMock(spec=BaseQueryEngine))

        # pylint: disable=protected-access
        self.assertEqual(backend.query_engine, backend._query_engine)
        backend.index.as_query_engine.assert_called_once()

    def test_query(self):
        backend = LlamaIndexBackend()
        backend.query = MagicMock(return_value=({'response': 'response text', 'response_object': Response('response text')}))
        user_input = [{"role": "user", "content": "test"}]

        result = backend.query(user_input)

        self.assertEqual(result['response'], "response text")

    def test_save(self):
        backend = LlamaIndexBackend()
        backend.index = MagicMock(spec=BaseIndex)
        backend.index.storage_context.persist = MagicMock()
        backend.save("test_storage_dir")
        # backend.index.storage_context.persist.assert_called_once_with(persist_dir="test_storage_dir/.indexes")
