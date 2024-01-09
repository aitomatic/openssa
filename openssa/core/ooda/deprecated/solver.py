from openssa.core.ooda.task import Task
from openssa.core.ooda.ooda_loop import OODALoop


class LLM:
    def get_response(self, prompt, history):
        pass


class History:
    def __init__(self):
        self.data = {}

    def update(self, step_name, findings):
        self.data[step_name] = findings

    def get_findings(self, step_name):
        return self.data.get(step_name, None)


class Solver:
    def __init__(self, tools, heuristics, llm):
        self.tools = tools
        self.heuristics = heuristics
        self.llm = llm
        self.history = History()

    def solve(self, task) -> Task.Result:
        if task is None:
            return Task.Result(status='Error', response='No task set')

        task.status = 'in_progress'
        heuristic = self.select_optimal_heuristic(task)

        if heuristic.should_subtask(task, self.llm, self.history):
            self.subtask(task, heuristic)
        else:
            self.run_ooda_loop(task, heuristic)

        return task.result

    def subtask(self, task, heuristic):
        subtasks = heuristic.decompose_task(task, self.llm, self.history)
        for subtask in subtasks:
            self.solve(subtask)

    def select_optimal_heuristic(self, task):
        return self.heuristics[0]  # TODO: for now, just return the first heuristic

    def run_ooda_loop(self, task, heuristic):
        ooda_loop = OODALoop()  # Initialize the OODA loop structure
        task.set_ooda_loop(ooda_loop)

        # Observe
        observation = self.observe(task)
        self.history.update('observe', observation)

        # Orient
        orientation = self.orient(observation)
        self.history.update('orient', orientation)

        # Decide
        decision = self.decide(orientation, heuristic)
        self.history.update('decide', decision)

        # Act
        action_result = self.act(decision, heuristic)
        self.history.update('act', action_result)

        # Create and set the result for the current task
        result = Task.Result(status='completed', response=action_result)
        task.set_result(result)
        return result

    def observe(self, task: Task):
        # Implement observation logic here, potentially using LLM and tools
        observation_prompt = f"Observe the situation for the task: {task.goal}"
        return self.llm.get_response(observation_prompt, self.history)

    def orient(self, observation):
        # Implement orientation logic here, potentially using LLM
        orient_prompt = f"Orient based on the observation: {observation}"
        return self.llm.get_response(orient_prompt, self.history)

    def decide(self, orientation, heuristic):
        # Implement decision logic here, potentially using heuristic and LLM
        decide_prompt = f"Decide the next action based on the orientation: {orientation}"
        return self.llm.get_response(decide_prompt, self.history)

    def act(self, decision, heuristic):
        # Implement action logic here, potentially using tools and LLM
        act_prompt = f"Act based on the decision: {decision}"
        return self.llm.get_response(act_prompt, self.history)
