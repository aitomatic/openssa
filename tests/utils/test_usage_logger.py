import unittest
from openssa.utils.llms import OpenAILLM


class TestUsageLogger(unittest.TestCase):
    def setUp(self):
        pass

    def test_with_openai_llm(self):
        llm = OpenAILLM()
        llm.get_response("say hello")


if __name__ == "__main__":
    unittest.main()
