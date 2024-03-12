import unittest
from openssa.core.ooda.ooda_loop import OODALoop


class TestOODALoop(unittest.TestCase):
    def test_run(self):
        # Create an instance of OODALoop
        goal = "Solve a problem"
        ooda_loop = OODALoop(goal)

        # Create a mock LLM and history
        class MockLLM:
            def get_response(self, prompt):
                return f"Response to: {prompt}"

        llm = MockLLM()
        history = []

        # Run the OODA loop
        output_data = ooda_loop.run(llm, history)

        self.assertIsNotNone(output_data)


if __name__ == '__main__':
    unittest.main()
