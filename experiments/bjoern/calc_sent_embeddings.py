from pathlib import Path

from data_models.embeddings_db import EmbeddingsDB
from data_models.message_db import MessageDB
from experiments.utils.paths import embeddings_path
from experiments.utils.paths import jsonl_path


def main():

    model_name = "paraphrase-albert-small-v2"
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    embeddings_shelve_path = embeddings_path.joinpath(
        f"sentences_1_{model_name}.shelve"
    )

    calc_sentence_embeddings(
        model_name=model_name,
        message_db=message_db,
        embeddings_shelve_path=embeddings_shelve_path,
    )


def calc_sentence_embeddings(
    model_name: str, message_db: MessageDB, embeddings_shelve_path: Path
):

    embedding_db = EmbeddingsDB(
        model_name=model_name, shelf_path=embeddings_shelve_path
    )

    sentences = message_db.get_sentences()
    embedding_db.add_sentences(sentences=sentences)


if __name__ == "__main__":
    main()
