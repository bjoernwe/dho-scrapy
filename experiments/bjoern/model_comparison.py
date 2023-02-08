import pickle
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from experiments.utils.paths import embeddings_path
from experiments.utils.paths import jsonl_path
from scraper.dho_scraper.categories import DhOCategory
from scraper.message_db.message_db import MessageDB


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
    compare_embeddings(model_names=model_names)


def compare_embeddings(model_names: List[str]):

    # Load practice logs of a certain user
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    author_id = "Linda ”Polly Ester” Ö"
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    pca_models = {}

    for model_name in model_names:

        # Load embeddings
        embd_path = embeddings_path.joinpath(f"embeddings_{model_name}.pkl")
        with open(str(embd_path), "rb") as f:
            embedding_db: Dict[int, np.ndarray] = pickle.load(f)

        # Calc PCA
        embeddings = np.vstack([embedding_db[msg.msg_id] for msg in practice_logs])
        pca_models[model_name] = PCA(n_components=10)
        pca_models[model_name].fit(embeddings)

    # Plot
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
    fig.show()


if __name__ == "__main__":
    main()
