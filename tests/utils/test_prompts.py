import unittest
from openssm.utils.prompts import Prompts  # replace 'your_module' with the actual name of the module where Prompts is defined


class TestPrompts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # pylint: disable=protected-access
        # Modify the _PROMPTS for testing
        Prompts._PROMPTS["openssm"]["core"]["slm"]["test_prompt"] = {"instruction": "This is a test instruction."}
        Prompts._PROMPTS["openssm"]["core"]["other_module"] = {"other_subindex": {"message": "This is another test message."}}

    def test_get_module_prompt(self):
        # Test case 1: Fetching the existing completion prompt
        result = Prompts.get_module_prompt('openssm.core.slm.base_slm', 'completion')
        expected = ("Complete this conversation with the assistant’s response, up to 2000 words. "
                    "Use this format: {\"role\": \"assistant\", \"content\": \"xxx\"}, "
                    "where 'xxx' is the response. "
                    "Make sure the entire response is valid JSON, xxx is only a string, "
                    "and no code of any kind, even if the prompt has code. "
                    "Escape quotes with \\:\n")
        self.assertEqual(result, expected)

        # Test case 2: Fetching the new test prompt
        result = Prompts.get_module_prompt('openssm.core.slm.test_prompt', 'instruction')
        expected = "This is a test instruction."
        self.assertEqual(result, expected)

        # Test case 3: Fetching another new test prompt
        result = Prompts.get_module_prompt('openssm.core.other_module.other_subindex', 'message')
        expected = "This is another test message."
        self.assertEqual(result, expected)

        # Test case 4: Fetching a base module prompt
        result = Prompts.get_module_prompt('openssm.core.slm.base_slm')
        self.assertIsInstance(result, dict)

        # Test case 5: Fetching a prompt that does not exist (invalid module)
        with self.assertRaises(ValueError):
            Prompts.get_module_prompt("openssm.core.slm.no_such_module")

        # Test case 6: Fetching a prompt that does not exist (invalid subindex)
        with self.assertRaises(ValueError):
            Prompts.get_module_prompt("openssm.core.slm.base_slm", "non_existent_subindex")
