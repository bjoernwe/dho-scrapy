from pathlib import Path

from data_models.embedders.embedder_mock import EmbedderMock
from data_models.embeddings_db import EmbeddingsDB
from data_models.textsnippet import TextSnippet


def test_embeddings_are_stored_persistently(tmp_path: Path):

    # GIVEN an EmbeddingDB and a sentence
    db_path = tmp_path.joinpath("emb_db.shelf")
    embedder_mock = EmbedderMock()
    emb_db = EmbeddingsDB(shelf_path=db_path, embedder=embedder_mock)
    sentence = TextSnippet(source_msg_id=123, idx=0, text="foo bar")

    # WHEN the sentence is added to the DB
    emb_db.add_snippets([sentence])

    # THEN the DB with sentence embedding can be restored again from disk
    restored_emb_db = EmbeddingsDB(shelf_path=db_path, embedder=embedder_mock)
    assert sentence.sid in restored_emb_db
