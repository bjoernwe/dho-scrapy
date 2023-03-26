import shelve
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Optional

import numpy as np
from tqdm import tqdm

from data_models.embedders.embedder import Embedder
from data_models.textsnippet import TextSnippet
from experiments.utils.paths import default_embeddings_path


class EmbeddingsDB:
    def __init__(
        self,
        shelf_path: Optional[Path] = None,
        embedder: Optional[Embedder] = None,
    ):
        self._embedder = embedder
        self._shelf_path = shelf_path or default_embeddings_path.joinpath(
            f"embeddings_{embedder.name}.shelf"
        )

    def __contains__(self, item):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            return item in shelf

    def __len__(self):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            return len(shelf)

    @property
    def shelf_path(self) -> Path:
        return self._shelf_path

    def add_snippets(self, snippets: Iterable[TextSnippet]):
        assert (
            self._embedder is not None
        ), "No Embedder object give. Provide it with __init__()!"
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            for sentence in tqdm(snippets):
                if sentence.sid in shelf:
                    continue
                embedding = self._embedder.embed(text=[sentence.text])
                shelf[sentence.sid] = embedding

    def __getitem__(self, sid: str) -> np.ndarray:
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            return shelf[sid]

    def get_embeddings(self, text_snippets: List[TextSnippet]) -> np.ndarray:
        return np.vstack([self[snippet.sid] for snippet in text_snippets])
