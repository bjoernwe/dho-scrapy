from pathlib import Path

from data_models.embeddings_db import EmbeddingsDB
from data_models.sentence import Sentence


def test_embeddings_are_stored_persistently(tmp_path: Path):

    # GIVEN an EmbeddingDB and a Sentence
    model_name = "paraphrase-albert-small-v2"
    db_path = tmp_path.joinpath("emb_db.shelve")
    emb_db = EmbeddingsDB(model_name=model_name, shelf_path=db_path)
    sentence = Sentence(msg_id=123, sentence_idx=0, sentence="foo bar")

    # WHEN the sentence is added to the DB
    emb_db.add_sentences([sentence])

    # THEN the DB with sentence embedding can be restored again from disk
    restored_emb_db = EmbeddingsDB(model_name=model_name, shelf_path=db_path)
    assert sentence.sid in restored_emb_db
