import atexit
import shelve
from pathlib import Path
from typing import Iterable
from typing import Optional

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from data_models.sentence import Sentence
from experiments.utils.paths import embeddings_path


class EmbeddingsDB:
    def __init__(self, model_name: str, shelve_path: Optional[Path] = None):
        self._model_name = model_name
        self._model = SentenceTransformer(model_name)
        self._shelve_path = shelve_path or embeddings_path.joinpath(
            f"sentences_{model_name}.shelve"
        )
        self._shelve = shelve.open(str(self._shelve_path), flag="c")
        atexit.register(self.close_shelve)

    def __contains__(self, item):
        return item in self._shelve

    def close_shelve(self):
        print("Closing shelve ...")
        self._shelve.close()

    def add_sentences(self, sentences: Iterable[Sentence]):

        try:

            for sentence in tqdm(sentences):

                if sentence.sid in self._shelve:
                    continue

                embedding = self._model.encode([sentence.sentence])
                self._shelve[sentence.sid] = embedding

        finally:
            print("Writing embeddings to to shelve file ...")
            self._shelve.sync()
