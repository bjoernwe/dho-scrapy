import shelve
from pathlib import Path
from typing import Iterable
from typing import Optional

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from data_models.sentence import Sentence
from experiments.utils.paths import default_embeddings_path


class EmbeddingsDB:
    def __init__(self, model_name: str, shelf_path: Optional[Path] = None):
        self._model_name = model_name
        self._model = SentenceTransformer(model_name)
        self._shelf_path = shelf_path or default_embeddings_path.joinpath(
            f"sentences_{model_name}.shelf"
        )

    def __contains__(self, item):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            return item in shelf

    def add_sentences(self, sentences: Iterable[Sentence]):
        with shelve.open(filename=str(self._shelf_path)) as shelf:
            for sentence in tqdm(sentences):
                if sentence.sid in shelf:
                    continue
                embedding = self._model.encode([sentence.sentence])
                shelf[sentence.sid] = embedding
