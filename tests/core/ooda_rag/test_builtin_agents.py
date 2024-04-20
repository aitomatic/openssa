import unittest
from unittest.mock import patch
from openssa.core.ooda_rag.builtin_agents import GoalAgent, AskUserAgent, AskUserAgentV2


class TestGoalAgent(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(GoalAgent, "execute", return_value="mocked_problem_statement")
    def test_execute(self, mock_execute):
        conversation = [
            {"role": "user", "content": "I want to buy a car"},
            {"role": "assistant", "content": "What is your budget?"},
            {"role": "user", "content": "My budget is 20000"},
            {"role": "assistant", "content": "Where do you live?"},
            {"role": "user", "content": "in Paris"},
            {"role": "assistant", "content": "Do you want a new or used car?"},
            {"role": "user", "content": "new one"},
        ]
        goal_agent = GoalAgent(conversation=conversation)
        problem_statement = goal_agent.execute("do something")
        mock_execute.assert_called_once_with("do something")
        assert problem_statement == "mocked_problem_statement"


class TestAskUserAgent(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(AskUserAgent, "execute")
    def test_execute(self, mock_execute):
        conversation = [
            {"role": "user", "content": "I want to buy a car"},
            {"role": "assistant", "content": "What is your budget?"},
            {"role": "user", "content": "My budget is 20000"},
            {"role": "assistant", "content": "Where do you live?"},
            {"role": "user", "content": "in Paris"},
            {"role": "assistant", "content": "Do you want a new or used car?"},
            {"role": "user", "content": "new one"},
        ]
        ask_user_agent = AskUserAgent(conversation=conversation)
        mock_execute.return_value = "Expected Result"
        task = "do something"

        # Act
        result = ask_user_agent.execute(task)

        # Assert
        mock_execute.assert_called_once_with(task)
        self.assertEqual(result, "Expected Result")


class TestAskUserAgentV2(unittest.TestCase):
    def setUp(self):
        pass

    @patch.object(AskUserAgentV2, "execute")
    def test_execute(self, mock_execute):
        conversation = [
            {"role": "user", "content": "I want to buy a car"},
            {"role": "assistant", "content": "What is your budget?"},
            {"role": "user", "content": "My budget is 20000"},
            {"role": "assistant", "content": "Where do you live?"},
            {"role": "user", "content": "in Paris"},
            {"role": "assistant", "content": "Do you want a new or used car?"},
            {"role": "user", "content": "new one"},
        ]
        ask_user_agent = AskUserAgentV2(conversation=conversation)
        mock_execute.return_value = "Expected Result"
        task = "do something"

        # Act
        result = ask_user_agent.execute(task)

        # Assert
        mock_execute.assert_called_once_with(task)
        self.assertEqual(result, "Expected Result")
