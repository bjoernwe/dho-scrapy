import shelve
from pathlib import Path
from typing import Iterable
from typing import Optional

from tqdm import tqdm

from data_models.embedders.embedder import Embedder
from data_models.embedders.embedder_transformer import EmbedderTransformer
from data_models.textsnippet import TextSnippet
from experiments.utils.paths import default_embeddings_path


class EmbeddingsDB:
    def __init__(
        self, shelf_path: Optional[Path] = None, embedder: Optional[Embedder] = None
    ):
        self._embedder = embedder or EmbedderTransformer()
        self._shelf_path = shelf_path or default_embeddings_path.joinpath(
            f"sentences_{embedder.name}.shelf"
        )

    def __contains__(self, item):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            return item in shelf

    @property
    def shelf_path(self) -> Path:
        return self._shelf_path

    def add_snippets(self, snippets: Iterable[TextSnippet]):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            for sentence in tqdm(snippets):
                if sentence.sid in shelf:
                    continue
                embedding = self._embedder.embed(text=[sentence.text])
                shelf[sentence.sid] = embedding
