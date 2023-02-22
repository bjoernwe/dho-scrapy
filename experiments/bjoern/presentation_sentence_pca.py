import pickle
from textwrap import wrap
from typing import Dict
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pandas import DataFrame
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA

from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.bjoern.sentence import Sentence
from experiments.utils.paths import data_path
from experiments.utils.paths import embeddings_path
from experiments.utils.paths import jsonl_path


def main():
    model_name = "paraphrase-albert-small-v2"
    plot_sentence_pca(model_name=model_name)


def plot_sentence_pca(model_name: str):

    # Load & filter messages
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        # .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        # .sorted_by_date()
        # .filter_message_length(min_num_words=3)
        .get_all_messages()
    )
    msg_ids = {msg.msg_id for msg in practice_logs}

    # Load & filter sentences
    sent_db_path = data_path.joinpath(f"sentences.pkl")
    print(f"Loading {sent_db_path} ...")
    with open(str(sent_db_path), "rb") as f:
        sent_db: Dict[str, Sentence] = pickle.load(f)
    sentence_ids = [
        sentence.sid
        for sentence in sent_db.values()
        if sentence.msg_id in msg_ids and len(sentence.sentence.split()) >= 3
    ]

    # Load & filter embeddings
    sent_emb_db_path = embeddings_path.joinpath(f"sent_embeddings_{model_name}.pkl")
    print(f"Loading {sent_emb_db_path} ...")
    with open(str(sent_emb_db_path), "rb") as f:
        sent_emb_db: Dict[str, np.ndarray] = pickle.load(f)
    print("Calculating embeddings ...")
    embeddings = np.vstack([sent_emb_db[sid] for sid in sentence_ids])

    # Calc PCA
    pca = PCA(n_components=100)
    print(f"Training PCA on {embeddings.shape[0]} embeddings ...")
    components = pca.fit_transform(embeddings)

    df = _create_dataframe(
        sent_db=sent_db, sentence_ids=sentence_ids, components=components
    )
    _plot(df=df)


def _create_dataframe(
    sent_db: Dict[str, Sentence], sentence_ids: List[str], components: np.ndarray
):

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        components, columns=[f"PCA_{i}" for i in range(components.shape[1])]
    )
    df["sid"] = sentence_ids
    df["sentence"] = [wrap(sent_db[sid].sentence, width=80)[0] for sid in sentence_ids]
    df = df.drop_duplicates(subset=["sentence"])
    print(df)

    return df


def _plot(df: DataFrame):

    fig = px.scatter(
        data_frame=df,
        x="PCA_0",
        y="PCA_1",
        hover_data=["sid", "sentence"],
    )

    fig.show()

    for i, title in [
        (0, '"Recognition" vs "Sleepiness"'),
        (1, '"Noticing" vs ???'),
        (2, '"Consistent Practice" vs "Weirdness"'),
        (3, '"Challenge" vs "Enjoyment"'),
        (4, '"Investigation" vs "Happiness"'),
        (5, '"Mental Action" vs "Bodily Discomfort"'),
    ]:

        num_bars = 20
        df = df.sort_values(f"PCA_{i}")

        fig = make_subplots(
            rows=1, cols=2, subplot_titles=["extremes (-)", "extremes (+)"]
        )

        fig.add_trace(
            go.Bar(
                x=df[::-1][f"PCA_{i}"][-num_bars:],
                text=df[::-1]["sentence"][-num_bars:],
                orientation="h",
                textposition="inside",
                textfont=dict(size=16),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=df[f"PCA_{i}"][-num_bars:],
                text=df["sentence"][-num_bars:],
                orientation="h",
                textposition="inside",
                textfont=dict(size=16, color="white"),
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title_text=f"PCA Component {i}: {title}",
            showlegend=False,
        )

        fig.show()


if __name__ == "__main__":
    main()
