import pickle
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from experiments.utils.paths import embeddings_path
from experiments.utils.paths import jsonl_path
from scraper.dho_scraper.categories import DhOCategory
from scraper.message_db.message_db import MessageDB


def main():
    model_name = "paraphrase-albert-small-v2"
    # model_name = "multi-qa-mpnet-base-dot-v1"
    # model_name = "paraphrase-MiniLM-L3-v2"
    plot_pca(model_name=model_name, show_plot=True)


def plot_pca(model_name: str, show_plot: bool = True):

    # Load embeddings
    embd_path = embeddings_path.joinpath(f"embeddings_{model_name}.pkl")
    with open(str(embd_path), "rb") as f:
        embedding_db: Dict[int, np.ndarray] = pickle.load(f)

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

    # Calc PCA
    pca = PCA(n_components=10)
    embeddings = np.vstack([embedding_db[msg.msg_id] for msg in practice_logs])
    components = pca.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        components, columns=[f"PCA_{i}" for i in range(components.shape[1])]
    )
    df["msg_id"] = [msg.msg_id for msg in practice_logs]
    df["msg"] = ["<br>".join(wrap(msg.msg, width=100)) for msg in practice_logs]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df.columns[0],
        y=df.columns[1],
        title=f"Text Embedding (Model: {model_name})",
        hover_data=["msg_id", "msg"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
