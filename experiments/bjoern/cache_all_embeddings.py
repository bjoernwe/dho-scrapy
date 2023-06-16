from experiments.experiment_helper import ExperimentHelper


def main():

    model_name = "paraphrase-albert-small-v2"

    for sentences_per_snippet in [0, 1, 3, 5, 10]:  # 0 = all sentences / full message

        calc_and_cache_embeddings(
            sentences_per_snippet=sentences_per_snippet,
            model_name=model_name,
        )


def calc_and_cache_embeddings(sentences_per_snippet: int, model_name: str):

    experiment = ExperimentHelper(
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
    )

    texts = experiment.message_db.get_snippet_texts(
        sentences_per_snippet=sentences_per_snippet
    )

    # Calculate embeddings (i.e., store in cache)
    print(
        f"Caching embeddings for {len(texts)} text snippets (sentences per snippet: {sentences_per_snippet} / model: {model_name}) ..."
    )
    _ = experiment.embedder.get_embeddings(texts=texts)


if __name__ == "__main__":
    main()
