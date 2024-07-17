from __future__ import annotations

from abc import ABC, abstractmethod


type AlgoIO = dict | list | str


class AbstractAlgo(ABC):
    @abstractmethod
    def execute(self, inputs: AlgoIO) -> AlgoIO:
        """Execute on given inputs and return outputs."""
