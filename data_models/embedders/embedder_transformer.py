from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from data_models.embedders.embedder import Embedder


class EmbedderTransformer(Embedder):
    def __init__(self, model_name: str = "paraphrase-albert-small-v2"):
        self._name = model_name
        self._model = SentenceTransformer(model_name_or_path=model_name)

    @property
    def name(self) -> str:
        return self._name

    def embed(self, text: List[str]) -> np.ndarray:
        return self._model.encode(sentences=text, convert_to_numpy=True)
