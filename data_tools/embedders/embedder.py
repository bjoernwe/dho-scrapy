from abc import ABC
from abc import abstractmethod
from typing import List

import numpy as np


class Embedder(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def embed(self, text: List[str]) -> np.ndarray:
        pass
