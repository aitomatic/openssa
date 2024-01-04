import unittest
from openssa.core.ooda.task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task("Test Goal")

    def test_add_subtask(self):
        subtask = Task("Subtask")
        self.task.add_subtask(subtask)

        self.assertTrue(self.task.has_subtasks())
        self.assertEqual(len(self.task.subtasks), 1)
        self.assertEqual(self.task.subtasks[0], subtask)
        self.assertEqual(subtask.parent, self.task)

    def test_has_ooda_loop(self):
        self.assertFalse(self.task.has_ooda_loop())

        self.task.ooda_loop = "OODA Loop"

        self.assertTrue(self.task.has_ooda_loop())
        self.assertEqual(self.task.ooda_loop, "OODA Loop")

    def test_result(self):
        self.assertEqual(self.task.status, 'pending')
        self.assertIsNone(self.task.result.response)
        self.assertEqual(len(self.task.result.references), 0)
        self.assertEqual(len(self.task.result.metrics), 0)
        self.assertEqual(len(self.task.result.additional_info), 0)

        self.task.status = 'completed'
        self.task.result.response = 'Test Response'
        self.task.result.references = ['Ref 1', 'Ref 2']
        self.task.result.metrics = {'metric1': 10, 'metric2': 20}
        self.task.result.additional_info = {'info1': 'Info 1', 'info2': 'Info 2'}

        self.assertEqual(self.task.status, 'completed')
        self.assertEqual(self.task.result.response, 'Test Response')
        self.assertEqual(len(self.task.result.references), 2)
        self.assertEqual(self.task.result.references[0], 'Ref 1')
        self.assertEqual(self.task.result.references[1], 'Ref 2')
        self.assertEqual(len(self.task.result.metrics), 2)
        self.assertEqual(self.task.result.metrics['metric1'], 10)
        self.assertEqual(self.task.result.metrics['metric2'], 20)
        self.assertEqual(len(self.task.result.additional_info), 2)
        self.assertEqual(self.task.result.additional_info['info1'], 'Info 1')
        self.assertEqual(self.task.result.additional_info['info2'], 'Info 2')


if __name__ == '__main__':
    unittest.main()
