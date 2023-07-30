"""
AbstractInferencer is the base class for all inferencers.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)  # needed to be added to a set
class AbstractInferencer(ABC):
    """
    The AbstractInferencer serves as the base for all concrete Inferencer
    classes.  The most common inferencer is simply an ML model, but it
    could also be a rule-based system, a fuzzy logic system, or any other
    system that can infer a response from a given input.
    """

    @abstractmethod
    def predict(self, input_data: dict) -> dict:
        """
        Returns a prediction based on the given input.
        """

    @abstractmethod
    def load(self, path: str):
        """
        Loads the inferencer or its parameters from the given path.
        """
