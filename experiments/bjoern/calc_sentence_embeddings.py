from typing import List

from data_tools.default_paths import default_cache_path
from data_tools.default_paths import default_jsonl_path
from data_tools.embedders.embedder_transformer import EmbedderTransformer
from data_tools.message_db import MessageDB


def main():

    model_name = "paraphrase-albert-small-v2"

    for sentences_per_snippet in [0, 1, 3, 5, 10]:  # 0 = all sentences / full message
        calc_and_cache_embeddings(
            sentences_per_snippet=sentences_per_snippet,
            model_name=model_name,
        )


def calc_and_cache_embeddings(sentences_per_snippet: int, model_name: str):

    # Get Embedder (with cache)
    cache_path = default_cache_path.joinpath(
        f"emb_snt_{sentences_per_snippet}_{model_name}.shelf"
    )
    embedder = EmbedderTransformer(model_name=model_name, cache_path=cache_path)

    # Calculate embeddings (i.e., store in cache)
    texts = _get_texts(sentences_per_snippet=sentences_per_snippet)
    print(
        f"Caching embeddings for {len(texts)} text snippets (sentenes per snippet: {sentences_per_snippet} / model: {model_name}) ..."
    )
    _ = embedder.get_embeddings(texts=texts)


def _get_texts(sentences_per_snippet: int) -> List[str]:
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    snippets = message_db.get_snippets(sentences_per_snippet=sentences_per_snippet)
    return [snippet.text for snippet in snippets]


if __name__ == "__main__":
    main()
