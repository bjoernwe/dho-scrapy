import pickle
from typing import Callable
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from data_tools.default_paths import default_cache_path
from data_tools.default_paths import default_jsonl_path
from data_tools.default_paths import get_default_cache_path
from data_tools.dho_categories import DhOCategory
from data_tools.embedders.embedder_transformer import EmbedderTransformer
from data_tools.message_db import MessageDB
from experiments.experiment_setup import ExperimentSetup


def main():

    model_names = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "all-distilroberta-v1",
        "all-MiniLM-L12-v2",
        "multi-qa-distilbert-cos-v1",
        "all-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
        "paraphrase-MiniLM-L3-v2",
        "distiluse-base-multilingual-cased-v1",
        "distiluse-base-multilingual-cased-v2",
    ]
    compare_embeddings(model_names=model_names, show_plot=True)


def compare_embeddings(
    model_names: List[str], sentence_per_snippet: int = 0, show_plot: bool = True
):

    # Load practice logs of a certain user
    author_id = "curious-frame"
    message_db = (
        MessageDB.from_file(jsonl_path=default_jsonl_path)
        .filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
    )
    snippets = message_db.get_snippets(sentences_per_snippet=sentence_per_snippet)
    texts = [snippet.text for snippet in snippets]

    pca_models = dict()

    for model_name in model_names:

        embeddings = EmbedderTransformer(
            model_name=model_name,
            cache_path=get_default_cache_path(
                sentences_per_snippet=sentence_per_snippet, model_name=model_name
            ),
        ).get_embeddings(texts=texts)

        # Calc PCA
        pca_models[model_name] = PCA(n_components=100).fit(embeddings)

    # Plot
    pca_models = _sort_dict(d=pca_models, key=lambda x: x[1].explained_variance_[0])
    pca_variances = np.array([pca.explained_variance_ for pca in pca_models.values()]).T
    df = pd.DataFrame(pca_variances, columns=list(pca_models.keys()))
    fig = px.line(
        data_frame=df,
        title="Explained variance of the first Principal Components",
        labels={
            "variable": "model",
            "index": "PCA component",
            "value": "explained variance (%)",
        },
    )
    if show_plot:
        fig.show()


def _sort_dict(d: dict, key: Callable):
    return dict(sorted(d.items(), key=key, reverse=True))


if __name__ == "__main__":
    main()
