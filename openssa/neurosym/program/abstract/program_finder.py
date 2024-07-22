from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.l2.util.lm.abstract import AnLM
    from openssa.neurosym.algo.abstract.algo import AbstractAlgo
    from openssa.neurosym.algo.abstract.algo_lib import AbstractAlgoLib


@dataclass
class AbstractAlgoFinder(ABC):
    lm: AnLM

    @abstractmethod
    def find_algo(self, problem: str, algo_lib: AbstractAlgoLib | None = None) -> AbstractAlgo:
        """Find algorithm for problem."""
