import pickle
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sksfa import SFA

from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.utils.paths import default_embeddings_path
from experiments.utils.paths import default_jsonl_path


def main():

    author = "Linda ”Polly Ester” Ö"

    model_name = "paraphrase-albert-small-v2"
    # model_name = "multi-qa-mpnet-base-dot-v1"
    # model_name = "paraphrase-MiniLM-L3-v2"

    plot_pca(author=author, model_name=model_name, show_plot=True)


def plot_pca(author: str, model_name: str, show_plot: bool = True):

    # Load practice logs of a certain user
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    # Load & calc embeddings
    embd_path = default_embeddings_path.joinpath(f"embeddings_{model_name}.pkl")
    with open(str(embd_path), "rb") as f:
        embedding_db: Dict[int, np.ndarray] = pickle.load(f)
    embeddings = np.vstack([embedding_db[msg.msg_id] for msg in practice_logs])

    # Calc PCA
    pca = PCA(n_components=30)
    embeddings = pca.fit_transform(embeddings)

    # Calc SFA
    sfa = SFA(n_components=3)
    slow_features = sfa.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        slow_features, columns=[f"SFA_{i}" for i in range(slow_features.shape[1])]
    )
    df["msg_id"] = [msg.msg_id for msg in practice_logs]
    df["date"] = [msg.date for msg in practice_logs]
    df["msg"] = ["<br>".join(wrap(msg.msg, width=100)) for msg in practice_logs]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df["date"],
        y=df["SFA_0"],
        title=f"SFA on Embedded Messages (Author: {author} / Model: {model_name})",
        hover_data=["msg_id", "msg"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
