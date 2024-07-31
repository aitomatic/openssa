class Heuristic:

    # Base class for heuristics
    def should_subtask(self, task, llm, history):
        pass

    def decompose_task(self, task, llm, history):
        pass
