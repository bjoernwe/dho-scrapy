import pickle
from math import log
from textwrap import wrap
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sksfa import SFA

from data_tools.default_paths import data_path
from data_tools.default_paths import default_cache_path
from data_tools.default_paths import default_jsonl_path
from data_tools.dho_categories import DhOCategory
from data_tools.message_db import MessageDB
from data_tools.textsnippet import TextSnippet


def main():
    author = "Linda ”Polly Ester” Ö"
    model_name = "paraphrase-albert-small-v2"
    plot_sentence_pca(author=author, model_name=model_name, show_plot=True)


def plot_sentence_pca(author: str, model_name: str, show_plot: bool = True):

    # Load message IDs
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )
    msg_ids = {msg.msg_id for msg in practice_logs}

    # Load sentences
    sent_db_path = data_path.joinpath(f"sentences.pkl")
    print(f"Loading {sent_db_path} ...")
    with open(str(sent_db_path), "rb") as f:
        sent_db: Dict[str, TextSnippet] = pickle.load(f)

    # Filter and sort sentences
    sentences = [
        sentence for sentence in sent_db.values() if sentence.source_msg_id in msg_ids
    ]
    sentences = sorted(
        sentences, key=lambda s: (message_db[s.source_msg_id].date, s.idx)
    )

    # Load embeddings
    sent_emb_db_path = default_cache_path.joinpath(f"sent_embeddings_{model_name}.pkl")
    print(f"Loading {sent_emb_db_path} ...")
    with open(str(sent_emb_db_path), "rb") as f:
        sent_emb_db: Dict[str, np.ndarray] = pickle.load(f)
    print("Calculating embeddings ...")
    embeddings = np.vstack([sent_emb_db[s.sid] for s in sentences])

    # Calc PCA
    pca = PCA(n_components=30)
    print(f"Training PCA on {embeddings.shape[0]} embeddings ...")
    embeddings = pca.fit_transform(embeddings)

    # Calc SFA
    sfa = SFA(n_components=3)
    print(f"Training SFA on {embeddings.shape[0]} embeddings ...")
    slow_features = sfa.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        slow_features, columns=[f"SFA_{i}" for i in range(slow_features.shape[1])]
    )
    df["sid"] = [s.sid for s in sentences]
    df["sentence_idx"] = [log(s.idx + 1) for s in sentences]
    df["date"] = [message_db[s.source_msg_id].date for s in sentences]
    df["sentence"] = ["<br>".join(wrap(s.text, width=100)) for s in sentences]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df["date"],
        y=df["SFA_0"],
        color="sentence_idx",
        title=f"Sentence Embedding (Model: {model_name})",
        hover_data=["sid", "sentence"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
