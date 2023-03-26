from pathlib import Path
from typing import Optional

import numpy as np

from data_tools.embedders.embedder import Embedder


class EmbedderMock(Embedder):
    def __init__(self, cache_path: Optional[Path] = None, dims: int = 32):
        super().__init__(cache_path=cache_path)
        self._dims = dims
        self.calls_to_calc = 0

    def _calc_embedding(self, text: str) -> np.ndarray:
        self.calls_to_calc += 1
        return np.random.randn(self._dims)
