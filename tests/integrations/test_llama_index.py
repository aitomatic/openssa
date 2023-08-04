import unittest
from unittest.mock import MagicMock, patch
from llama_index import Response
from llama_index.indices.base import BaseIndex
from llama_index.indices.query.base import BaseQueryEngine
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.slm.base_slm import PassthroughSLM
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.slm import GPT3ChatCompletionSLM
from openssm.integrations.llama_index.ssm import BaseLlamaIndexSSM, LlamaIndexSSM, GPT3LlamaIndexSSM


class TestSSMClasses(unittest.TestCase):
    def test_base_llama_index_ssm(self):
        slm = MagicMock(spec=AbstractSLM)
        backend = MagicMock(spec=AbstractBackend)
        ssm = BaseLlamaIndexSSM(slm, [backend])

        self.assertIsInstance(ssm.llama_backend, LlamaIndexBackend)
        self.assertEqual(ssm.get_llama_backend(), ssm.llama_backend)

        with patch.object(ssm.llama_backend, 'read_directory') as mock_read_dir:
            ssm.read_directory("test_directory")
            mock_read_dir.assert_called_once_with("test_directory", False)

    def test_llama_index_ssm(self):
        backend = MagicMock(spec=AbstractBackend)
        ssm = LlamaIndexSSM([backend])

        self.assertIsInstance(ssm.llama_backend, LlamaIndexBackend)
        self.assertIsInstance(ssm.slm, PassthroughSLM)

    def test_gpt3_llama_index_ssm(self):
        backend = MagicMock(spec=AbstractBackend)
        ssm = GPT3LlamaIndexSSM(backends=[backend])

        self.assertIsInstance(ssm.slm, GPT3ChatCompletionSLM)

class TestBackend(unittest.TestCase):
    def test_query_engine(self):
        backend = LlamaIndexBackend()
        backend.index = MagicMock(spec=BaseIndex)
        backend.index.as_query_engine = MagicMock(return_value=MagicMock(spec=BaseQueryEngine))

        # pylint: disable=protected-access
        self.assertEqual(backend.query_engine, backend._query_engine)
        backend.index.as_query_engine.assert_called_once()

    def test_query2_no_index(self):
        backend = LlamaIndexBackend()
        backend.index = None
        user_input = [{"role": "user", "content": "test"}]

        result, response = backend.query2(user_input)

        self.assertEqual(result[0]['response'], "I'm sorry, I don't have an index to query. Please load something first.")
        self.assertEqual(response, None)

    def test_query(self):
        backend = LlamaIndexBackend()
        backend.query2 = MagicMock(return_value=(["response text"], Response('response text')))
        user_input = [{"role": "user", "content": "test"}]

        result = backend.query(user_input)

        self.assertEqual(result, ["response text"])

    def test_save(self):
        backend = LlamaIndexBackend()
        backend.index = MagicMock(spec=BaseIndex)
        backend.index.storage_context.persist = MagicMock()
        backend.save("test_storage_dir")
        backend.index.storage_context.persist.assert_called_once_with(persist_dir="test_storage_dir/.indexes")
