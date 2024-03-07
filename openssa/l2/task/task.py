"""Task."""


from .abstract import AbstractTask


class Task(AbstractTask):
    """Task."""

    def execute(self):
        if self.all_dependencies_satisfied():
            self.select_agent()
            self.status = 'in progress'
            try:
                self.result = self.agent.execute_task(self.ask)
                self.status = 'completed'
            except Exception as e:  # pylint: disable=broad-exception-caught
                self.status = 'failed'
                self.result = str(e)
        else:
            self.status = 'waiting for dependencies'

    def all_dependencies_satisfied(self):
        # Check if all dependencies are completed
        return all(dep.status == 'completed' for dep in self.dependencies)

    def select_agent(self):
        # Logic to select the most appropriate agent based on the task's requirements
        pass


class UnitTask(Task):
    def execute(self):
        # Direct execution logic for UnitTasks, potentially overriding Task's execute method
        pass


# Agent interface (to be implemented by each agent)
class Agent:
    def execute_task(self, task_description):
        pass
