from typing import Iterator
from typing import List

import numpy as np

from data_models.embedders.embedder import Embedder


class EmbedderMock(Embedder):
    def __init__(self, dims: int = 32):
        self._dims = dims

    @property
    def name(self) -> str:
        return "mock"

    def embed(self, text: List[str]) -> np.ndarray:
        return np.random.randn(self._dims)
