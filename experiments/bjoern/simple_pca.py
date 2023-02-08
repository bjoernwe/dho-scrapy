import pickle
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from dho_scraper.categories import DhOCategory
from experiments.utils.messages import message_db
from experiments.utils.paths import model_path


def main():
    # model_name = "all-MiniLM-L12-v2"
    model_name = "multi-qa-mpnet-base-dot-v1"
    plot_pca(model_name=model_name)


def plot_pca(model_name: str):

    # Load embeddings
    embeddings_path = model_path.joinpath(f"embeddings_{model_name}.pkl")
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
        title="Text Embedding",
        hover_data=["msg_id", "msg"],
    )
    fig.show()


if __name__ == "__main__":
    main()