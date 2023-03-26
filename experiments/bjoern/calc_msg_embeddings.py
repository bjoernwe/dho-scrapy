from typing import List

from data_tools.default_paths import default_embeddings_path
from data_tools.default_paths import default_jsonl_path
from data_tools.embedders.embedder_transformer import EmbedderTransformer
from data_tools.embeddings_db import EmbeddingsDB
from data_tools.message_db import MessageDB
from data_tools.textsnippet import TextSnippet


def main():

    model_names = [
        # "all-mpnet-base-v2",
        # "multi-qa-mpnet-base-dot-v1",
        # "all-distilroberta-v1",
        # "all-MiniLM-L12-v2",
        # "multi-qa-distilbert-cos-v1",
        # "all-MiniLM-L6-v2",
        # "multi-qa-MiniLM-L6-cos-v1",
        # "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        # "paraphrase-multilingual-MiniLM-L12-v2",
        # "paraphrase-MiniLM-L3-v2",
        # "distiluse-base-multilingual-cased-v1",
        # "distiluse-base-multilingual-cased-v2",
    ]

    snippets = _get_snippets()

    for model_name in model_names:
        calc_and_store_embeddings(snippets=snippets, model_name=model_name)


def calc_and_store_embeddings(snippets: List[TextSnippet], model_name: str):
    embeddings_db = _get_embeddings_db(model_name=model_name)
    print(
        f'Calculate embeddings for {len(snippets)} messages with model "{model_name}" ...'
    )
    embeddings_db.add_snippets(snippets=snippets)


def _get_snippets() -> List[TextSnippet]:
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    snippets = message_db.get_snippets(sentences_per_snippet=0)
    return snippets


def _get_embeddings_db(model_name: str) -> EmbeddingsDB:
    shelf_path = default_embeddings_path.joinpath(f"msg_emb_{model_name}.shelf")
    embedder = EmbedderTransformer(model_name=model_name)
    embeddings_db = EmbeddingsDB(shelf_path=shelf_path, embedder=embedder)
    return embeddings_db


if __name__ == "__main__":
    main()
