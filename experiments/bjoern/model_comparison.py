import pickle
from pathlib import Path
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from dho_scraper.categories import DhOCategory
from message_db.message_db import MessageDB


def compare_embeddings(model_names: List[str]):

    # Load messages
    data_path = Path().resolve().parent.parent.joinpath("data")
    jsonl_path = data_path.joinpath("messages.jsonl")
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)

    # Load practice logs of a certain user
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
        embeddings_path = data_path.joinpath(f"models/embeddings_{model_name}.pkl")
        with open(str(embeddings_path), "rb") as f:
            embedding_db: Dict[int, np.ndarray] = pickle.load(f)

        # Calc PCA
        embeddings = np.vstack([embedding_db[msg.msg_id] for msg in practice_logs])
        pca_models[model_name] = PCA(n_components=10)
        pca_models[model_name].fit(embeddings)

    # Plot
    pca_variances = np.array([pca.explained_variance_ for pca in pca_models.values()]).T
    df = pd.DataFrame(pca_variances, columns=list(pca_models.keys()))
    fig = px.line(df)
    fig.show()


if __name__ == "__main__":

    model_names = ["all-MiniLM-L12-v2", "multi-qa-mpnet-base-dot-v1"]

    compare_embeddings(model_names=model_names)
