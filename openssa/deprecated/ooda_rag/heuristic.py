from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union


class Heuristic(ABC):
    """
    Abstract base class for defining heuristics.
    """

    @abstractmethod
    def apply_heuristic(self, task: str) -> Union[list, dict]:
        """
        Apply the heuristic to the given task and return a list of subtasks.
        """
        pass


class TaskDecompositionHeuristic(Heuristic):
    """
    Base class for task decomposition heuristics.
    """

    def __init__(self, heuristic_rules: dict[str, list[str]]) -> None:
        """
        Initialize the heuristic with a dictionary of heuristic rules.
        """
        self.heuristic_rules = heuristic_rules

    def apply_heuristic(self, task: str) -> list:
        """
        Apply the heuristic rules to decompose the task into subtasks.
        """
        subtasks = []
        for keyword, heuristic_subtasks in self.heuristic_rules.items():
            if keyword.lower() in task.lower():
                subtasks.extend(heuristic_subtasks)
        return subtasks


class DefaultOODAHeuristic(Heuristic):
    def apply_heuristic(self, task: str) -> dict:
        observe = {
            "thought": f"Gather information from research document to solve the task \n {task}",
            "calls": [
                {"tool_name": "research_documents", "parameters": {"task": task}}
            ],
        }
        orient = {
            "thought": ("Analyze the information gathered from research documents. "),
            "calls": [],
        }
        decide = {
            "thought": "Decide using the information gathered from research documents",
            "calls": [],
        }
        act = {
            "thought": "Add the information to the task history to solve the task",
            "calls": [],
        }
        return {"observe": observe, "orient": orient, "decide": decide, "act": act}


class GPTOODAHeuristic(Heuristic):
    def __init__(self, heuristics: dict) -> None:
        """
        Initialize the heuristic with a dictionary of heuristic rules.
        """
        self.heuristics = heuristics

    def apply_heuristic(self, task: str) -> list:
        """
        Apply the heuristic rules to decompose the task into subtasks.
        """
        print(task)


class HeuristicSet:
    """
    A set of heuristics.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize the heuristic set.
        """
        self.task_heuristics = kwargs.get(
            "task_heuristics", TaskDecompositionHeuristic({})
        )
        self.ooda_heuristics = kwargs.get("ooda_heuristics", DefaultOODAHeuristic())
        self.highest_priority_heuristic = kwargs.get("highest_priority_heuristic", "")
        self.comm_heuristic = kwargs.get("comm_heuristic", "")
        self.ask_user_heuristic = kwargs.get("ask_user_heuristic", "")
        self.goal_heuristics = kwargs.get("goal_heuristics", "")
