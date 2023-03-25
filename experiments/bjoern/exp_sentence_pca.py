import pickle
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from data_models.sentence import Sentence
from experiments.utils.paths import data_path
from experiments.utils.paths import default_embeddings_path
from experiments.utils.paths import default_jsonl_path


def main():
    author = "Linda ”Polly Ester” Ö"
    model_name = "paraphrase-albert-small-v2"
    plot_sentence_pca(author=author, model_name=model_name, show_plot=True)


def plot_sentence_pca(author: str, model_name: str, show_plot: bool = True):

    # Load & filter messages
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )
    msg_ids = {msg.msg_id for msg in practice_logs}

    # Load & filter sentences
    sent_db_path = data_path.joinpath(f"sentences.pkl")
    print(f"Loading {sent_db_path} ...")
    with open(str(sent_db_path), "rb") as f:
        sent_db: Dict[str, Sentence] = pickle.load(f)
    sentence_ids = [
        sentence.sid for sentence in sent_db.values() if sentence.msg_id in msg_ids
    ]

    # Load & filter embeddings
    sent_emb_db_path = default_embeddings_path.joinpath(
        f"sent_embeddings_{model_name}.pkl"
    )
    print(f"Loading {sent_emb_db_path} ...")
    with open(str(sent_emb_db_path), "rb") as f:
        sent_emb_db: Dict[str, np.ndarray] = pickle.load(f)
    print("Calculating embeddings ...")
    embeddings = np.vstack([sent_emb_db[sid] for sid in sentence_ids])

    # Calc PCA
    pca = PCA(n_components=100)
    print(f"Training PCA on {embeddings.shape[0]} embeddings ...")
    components = pca.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        components, columns=[f"PCA_{i}" for i in range(components.shape[1])]
    )
    df["sid"] = sentence_ids
    df["sentence"] = [
        "<br>".join(wrap(sent_db[sid].sentence, width=100)) for sid in sentence_ids
    ]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df.columns[0],
        y=df.columns[1],
        title=f"PCA of Sentence Embeddings (Author: {author} / Model: {model_name})",
        hover_data=["sid", "sentence"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
