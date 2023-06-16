from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from data_tools.embedders.embedder import Embedder


class TransformerEmbedder(Embedder):
    def __init__(self, model_name: str, cache_path: Path):
        super().__init__(cache_path=cache_path)
        self._model = SentenceTransformer(model_name_or_path=model_name)

    def _calc_embedding(self, text: str) -> np.ndarray:
        return self._model.encode(sentences=[text], convert_to_numpy=True)
