from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.neurosym.algo.abstract.algo import AbstractAlgo


class AbstractAlgoLib(ABC):
    @abstractmethod
    def add_algo(self, name: str, desc: str, algo: AbstractAlgo):
        """Add algorithm to library with unique identifying name & informative description."""
