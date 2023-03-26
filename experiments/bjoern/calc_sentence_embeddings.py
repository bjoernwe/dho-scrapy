from typing import List

from data_models.embedders.embedder_transformer import EmbedderTransformer
from data_models.embeddings_db import EmbeddingsDB
from data_models.message_db import MessageDB
from data_models.textsnippet import TextSnippet
from experiments.utils.paths import default_embeddings_path
from experiments.utils.paths import default_jsonl_path


def main(model_name: str = "paraphrase-albert-small-v2"):

    for sentences_per_snippet in [1, 3, 5, 10]:
        embeddings_db = EmbeddingsDB(
            shelf_path=default_embeddings_path.joinpath(
                f"{sentences_per_snippet}_sent_emb_{model_name}.shelf"
            ),
            embedder=EmbedderTransformer(model_name=model_name),
        )
        snippets = _get_snippets(sentences_per_snippet=sentences_per_snippet)
        embeddings_db.add_snippets(snippets=snippets)


def _get_snippets(sentences_per_snippet: int) -> List[TextSnippet]:
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    snippets = message_db.get_snippets(sentences_per_snippet=sentences_per_snippet)
    return snippets


if __name__ == "__main__":
    main()
