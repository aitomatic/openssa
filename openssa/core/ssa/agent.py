from openssa.core.ooda.task import Task
from openssa.core.ooda.ooda_loop import OODALoop
from openssa.core.ooda.heuristic import Heuristic
from openssa.utils.llms import OpenAILLM


class Agent:
    def __init__(
        self,
        llm=OpenAILLM(),
        resources=None,
        short_term_memory=None,
        long_term_memory=None,
        heuristics=None,
    ):
        self.llm = llm
        self.resources = resources
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory
        self.heuristics = heuristics

    def solve(self, objective):
        task = Task(objective)
        return self.solve_task(task)

    def solve_task(self, task):
        if task is None:
            return Task.Result(status="Error", response="No task set")

        task.status = "in_progress"
        heuristic = self.select_optimal_heuristic(task)

        if heuristic.should_subtask(task, self.llm, self.short_term_memory):
            self.subtask(task, heuristic)
        else:
            self.run_ooda_loop(task, heuristic)

        return task.result

    def select_optimal_heuristic(self, task):
        if self.heuristics is None or len(self.heuristics) == 0:
            return Heuristic()

        return self.heuristics[0]  # TODO: for now, just return the first heuristic

    def subtask(self, task, heuristic):
        task.status = "subtasking"

        task.subtasks = heuristic.decompose_task(task, self.llm, self.short_term_memory)
        results = []
        for subtask in task.subtasks:
            results.append(self.solve(subtask))

        task.result = Task.Result(
            status="completed", response="Subtasking complete", additional_info=results
        )

    def run_ooda_loop(self, task, heuristic):
        task.status = "ooda_looping"
        task.ooda_loop = OODALoop(task.goal)
        output = task.ooda_loop.run(self.llm, [])
        task.result = Task.Result(status="completed", response=output)

    def update_memory(self, key, value, memory_type="short"):
        if memory_type == "short":
            self.short_term_memory.update(key, value)
        else:
            self.long_term_memory.update(key, value)
