import pickle
from pathlib import Path
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from dho_scraper.categories import DhOCategory
from message_db.message_db import MessageDB


def plot_pca(model_name: str):

    # Load messages
    data_path = Path().resolve().parent.parent.joinpath("data")
    jsonl_path = data_path.joinpath("messages.jsonl")
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)

    # Load embeddings
    embeddings_path = data_path.joinpath(f"models/embeddings_{model_name}.pkl")
    with open(str(embeddings_path), "rb") as f:
        embedding_db: Dict[int, np.ndarray] = pickle.load(f)

    # Load practice logs of a certain user
    author_id = "Linda ”Polly Ester” Ö"
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    # Calc PCA
    pca = PCA(n_components=10)
    embeddings = np.vstack([embedding_db[msg.msg_id] for msg in practice_logs])
    components = pca.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        components, columns=[f"pca_{i}" for i in range(components.shape[1])]
    )
    df["msg_id"] = [msg.msg_id for msg in practice_logs]
    df["msg"] = ["<br>".join(wrap(msg.msg, width=100)) for msg in practice_logs]
    print(df)

    # Plot
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1], hover_data=["msg_id", "msg"])
    fig.show()


if __name__ == "__main__":
    # model_name = "all-MiniLM-L12-v2"
    model_name = "multi-qa-mpnet-base-dot-v1"

    plot_pca(model_name=model_name)
