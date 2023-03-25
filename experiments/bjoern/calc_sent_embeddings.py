from pathlib import Path

from data_models.embeddings_db import EmbeddingsDB
from data_models.message_db import MessageDB
from experiments.utils.paths import default_embeddings_path
from experiments.utils.paths import default_jsonl_path


def main(
    jsonl_path: Path = default_jsonl_path,
    model_name: str = "paraphrase-albert-small-v2",
    window_size: int = 1,
):

    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    embeddings_shelve_path = default_embeddings_path.joinpath(
        f"sentences_{window_size}_{model_name}.shelf"
    )

    calc_sentence_embeddings(
        model_name=model_name,
        message_db=message_db,
        embeddings_shelve_path=embeddings_shelve_path,
        window_size=window_size,
    )


def calc_sentence_embeddings(
    model_name: str,
    message_db: MessageDB,
    embeddings_shelve_path: Path,
    window_size: int,
):

    embedding_db = EmbeddingsDB(
        model_name=model_name, shelf_path=embeddings_shelve_path
    )

    sentences = message_db.get_sentences(window_size=window_size)
    embedding_db.add_sentences(sentences=sentences)


if __name__ == "__main__":
    main()
