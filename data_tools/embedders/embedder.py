import hashlib
import shelve
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Iterator
from typing import Optional

import numpy as np
from tqdm import tqdm

from data_tools.default_paths import default_cache_path


class Embedder(ABC):
    """
    Wraps around an embedding function and caches the result on disk.
    """

    def __init__(self, cache_path: Optional[Path] = None):
        self._cache_path: Path = cache_path or default_cache_path.joinpath(
            "embeddings.shelf"
        )

    @abstractmethod
    def _calc_embedding(self, text: str) -> np.ndarray:
        pass

    def get_embedding(self, text: str) -> np.ndarray:

        text_hash = self._calc_hash(text=text)

        with shelve.open(str(self._cache_path)) as cache:

            if text_hash in cache:
                return cache[text_hash]

            embedding = self._calc_embedding(text=text)
            cache[text_hash] = embedding

            return embedding

    def get_embeddings(self, texts: Iterator[str]) -> np.ndarray:

        embeddings = []

        with shelve.open(str(self._cache_path)) as cache:

            for text in tqdm(texts):

                text_hash = self._calc_hash(text=text)

                if text_hash in cache:
                    embedding = cache[text_hash]
                else:
                    embedding = self._calc_embedding(text=text)
                    cache[text_hash] = embedding

                embeddings.append(embedding)

        return np.vstack(embeddings)

    @staticmethod
    def _calc_hash(text: str) -> str:
        return hashlib.md5(text.encode("UTF-8")).hexdigest()
