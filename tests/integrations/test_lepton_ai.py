import unittest
from unittest.mock import MagicMock
from openssm.core.backend.rag_backend import AbstractRAGBackend
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.integrations.lepton_ai.ssm import SSM as LeptonAISSM, RAGSSM as LeptonAIRAGSSM
from openssm.utils.config import Config

Config.LEPTONAI_API_URL = "test_url"
Config.LEPTONAI_API_KEY = "test_key"

class TestSSM(unittest.TestCase):
    def test_constructor_default_values(self):
        adapter = MagicMock(spec=AbstractAdapter)
        slm = LeptonAISSM(adapter=adapter)
        self.assertIsNotNone(slm.slm)  # LeptonSLM is assigned
        self.assertEqual(slm.adapter, adapter)
        self.assertIsNotNone(slm.backends)
        self.assertIsNotNone(slm.name)


class TestRAGSSM(unittest.TestCase):
    def test_constructor_default_values(self):
        rag_backend = MagicMock(spec=AbstractRAGBackend)
        slm = LeptonAIRAGSSM(rag_backend=rag_backend, name="test_name", storage_dir="test_dir")
        self.assertIsNotNone(slm.slm)  # LeptonSLM is assigned
        self.assertEqual(slm.rag_backend, rag_backend)
        self.assertEqual(slm.name, "test_name")
        self.assertEqual(slm.storage_dir, "test_dir")

    def test_constructor_with_default_backend(self):
        slm = LeptonAIRAGSSM(name="test_name", storage_dir="test_dir")
        self.assertIsNotNone(slm.rag_backend)  # LlamaIndexBackend is assigned
