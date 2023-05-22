from pathlib import Path
from typing import Optional

from data_tools.default_paths import default_jsonl_path
from data_tools.default_paths import get_default_cache_path
from data_tools.embedders.embedder import Embedder
from data_tools.embedders.embedder_transformer import TransformerEmbedder
from data_tools.message_db import MessageDB


class ExperimentHelper:
    """
    A helper class for setting up common objects for an experiment:
    - a MessageDB and
    - an EmbedderTransformer with cache
    """

    def __init__(
        self,
        model_name: str,
        sentences_per_snippet: int,
        jsonl_path: Optional[Path] = None,
    ):

        self._model_name = model_name
        self._sentences_per_snippet = sentences_per_snippet

        jsonl_path = jsonl_path or default_jsonl_path
        self._msg_db = MessageDB.from_file(jsonl_path=jsonl_path)

        cache_path = get_default_cache_path(
            sentences_per_snippet=sentences_per_snippet, model_name=model_name
        )
        self._embedder = TransformerEmbedder(
            model_name=model_name, cache_path=cache_path
        )

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def sentences_per_snippet(self) -> int:
        return self._sentences_per_snippet

    @property
    def message_db(self) -> MessageDB:
        return self._msg_db

    @property
    def embedder(self) -> Embedder:
        return self._embedder
