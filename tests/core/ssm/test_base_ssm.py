import unittest
from unittest.mock import MagicMock
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.slm.abstract_slm import AbstractSLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.core.backend.abstract_backend import AbstractBackend

class TestBaseSSM(unittest.TestCase):

    def setUp(self):
        self.base_ssm = BaseSSM()

    def test_conversations(self):
        self.assertEqual(self.base_ssm.conversations, {})
        conversation_id = "conv_id_1"
        conversation_data = [{'role': 'user', 'content': 'message1'}, {'role': 'assistant', 'content': 'message2'}]
        # pylint: disable=unsupported-assignment-operation
        self.base_ssm.conversations[conversation_id] = conversation_data
        # pylint: disable=unsubscriptable-object
        self.assertEqual(self.base_ssm.conversations[conversation_id], conversation_data)
        self.assertIsInstance(self.base_ssm.conversations, dict)
        for conversation in self.base_ssm.conversations.values():
            self.assertIsInstance(conversation, list)
            for item in conversation:
                self.assertIn('role', item)
                self.assertIn('content', item)
                self.assertIn(item['role'], ['system', 'user', 'assistant'])

    def test_slm(self):
        self.assertIsInstance(self.base_ssm.slm, AbstractSLM)

    def test_adapter(self):
        self.assertIsInstance(self.base_ssm.adapter, AbstractAdapter)

    def test_backends(self):
        self.assertIsInstance(self.base_ssm.backends, list)
        for backend in self.base_ssm.backends:
            self.assertIsInstance(backend, AbstractBackend)

    def test_name(self):
        self.assertIsInstance(self.base_ssm.name, str)

    def test_discuss(self):
        user_input = [{'role': 'user', 'content': 'message1'}]
        conversation_id = "conv_id_1"
        self.base_ssm.custom_discuss = MagicMock(return_value=(None, user_input))
        self.base_ssm.update_conversation = MagicMock()
        # pylint: disable=unused-variable
        # flake8: noqa
        result = self.base_ssm.discuss(user_input, conversation_id)
        self.base_ssm.custom_discuss.assert_called_with(user_input, self.base_ssm.get_conversation(conversation_id))
        self.base_ssm.update_conversation.assert_called_with(user_input, None, conversation_id)

    def test_get_conversation(self):
        conversation_id = "conv_id_1"
        self.assertEqual(self.base_ssm.get_conversation(conversation_id), [])
        # pylint: disable=unsupported-assignment-operation
        self.base_ssm.conversations[conversation_id] = [{'role': 'user', 'content': 'message'}]
        self.assertEqual(self.base_ssm.get_conversation(conversation_id), [{'role': 'user', 'content': 'message'}])

    def test_api_call(self):
        self.base_ssm.adapter.api_call = MagicMock(return_value='result')
        self.assertEqual(self.base_ssm.api_call('function_name', 'arg1'), 'result')

    def test_facts(self):
        with self.assertRaises(AttributeError):
            self.base_ssm.adapter.facts = ['fact1']

    def test_inferencers(self):
        with self.assertRaises(AttributeError):
            self.base_ssm.adapter.inferencers = ['inferencer1']

    def test_heuristics(self):
        with self.assertRaises(AttributeError):
            self.base_ssm.adapter.heuristics = ['heuristic1']

    def test_select_methods(self):
        self.base_ssm.adapter.select_facts = MagicMock(return_value=['fact1'])
        self.base_ssm.adapter.select_inferencers = MagicMock(return_value=['inferencer1'])
        self.base_ssm.adapter.select_heuristics = MagicMock(return_value=['heuristic1'])
        self.assertEqual(self.base_ssm.select_facts({}), ['fact1'])
        self.assertEqual(self.base_ssm.select_inferencers({}), ['inferencer1'])
        self.assertEqual(self.base_ssm.select_heuristics({}), ['heuristic1'])

    def test_infer(self):
        self.base_ssm.adapter.infer = MagicMock(return_value=['result'])
        self.assertEqual(self.base_ssm.infer({}), ['result'])

    def test_storage_dir(self):
        # pylint: disable=protected-access
        self.base_ssm._storage_dir = "storage_dir"
        self.assertEqual(self.base_ssm.storage_dir, "storage_dir")

    def test_save(self):
        self.base_ssm.slm.save = MagicMock()
        self.base_ssm.adapter.save = MagicMock()
        self.base_ssm.adapter.enumerate_backends = MagicMock()
        self.base_ssm.save()
        self.base_ssm.slm.save.assert_called()
        self.base_ssm.adapter.save.assert_called()
        self.base_ssm.adapter.enumerate_backends.assert_called()

    def test_load(self):
        self.base_ssm.slm.load = MagicMock()
        self.base_ssm.adapter.load = MagicMock()
        self.base_ssm.adapter.enumerate_backends = MagicMock()
        self.base_ssm.load()
        self.base_ssm.slm.load.assert_called()
        self.base_ssm.adapter.load.assert_called()
        self.base_ssm.adapter.enumerate_backends.assert_called()

    def test_custom_discuss(self):
        user_input = [{'role': 'user', 'content': 'message'}]
        reply = {'role': 'assistant', 'content': 'reply'}
        self.base_ssm.slm.do_discuss = MagicMock(return_value=reply)
        response, actual_input = self.base_ssm.custom_discuss(user_input, [])
        self.assertEqual(response, reply)
        self.assertEqual(actual_input, user_input)

    def test_reset_memory(self):
        self.base_ssm.slm.reset_memory = MagicMock()
        self.base_ssm.reset_memory()
        # pylint: disable=protected-access
        self.assertIsNone(self.base_ssm._conversations)
        self.base_ssm.slm.reset_memory.assert_called()

    def test_conversation_history(self):
        self.base_ssm.reset_memory()
        self.base_ssm.conversation_tracking = True
        user_input1 = {'role': 'user', 'content': 'message1'}
        user_input2 = {'role': 'user', 'content': 'message2'}
        expected_reply = {'role': 'assistant', 'content': 'Hello, as the base implementation of SLM, this is all I can say.'}

        self.base_ssm.discuss([user_input1])
        self.base_ssm.discuss([user_input2])

        expected_conversation = [user_input1, expected_reply, user_input2, expected_reply]
        self.assertEqual(self.base_ssm.get_conversation(self.base_ssm.DEFAULT_CONVERSATION_ID), expected_conversation)
