import unittest
from openssa.core.ssa.agent import Agent
from openssa.core.ooda.task import Task
from openssa.core.ooda.heuristic import Heuristic


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()
        self.task = Task("Test Task")
        self.heuristic = Heuristic()

    def set_dummy_result(self, task):
        task.result = Task.Result(status='completed', response='Test Response')

    def test_subtask(self):
        subtasks = [Task("Subtask 1"), Task("Subtask 2"), Task("Subtask 3")]
        self.heuristic.decompose_task = lambda task, llm, memory: subtasks  # noqa: ARG005
        self.agent.solve = self.set_dummy_result

        self.agent.subtask(self.task, self.heuristic)

        self.assertEqual("completed", self.task.result.status)
        self.assertEqual(len(self.task.subtasks), len(subtasks))
        for i, subtask in enumerate(self.task.subtasks):
            self.assertEqual(subtask, subtasks[i])


if __name__ == '__main__':
    unittest.main()
