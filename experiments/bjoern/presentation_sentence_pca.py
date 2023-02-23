import pickle
from textwrap import wrap
from typing import Dict
from typing import List
from typing import Set

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
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
    _plot_sentence_pca(model_name=model_name)


def _plot_sentence_pca(model_name: str):

    message_ids = _get_relevant_message_ids()
    print(f"Got {len(message_ids)} messages.")

    sentence_db = _get_sentence_db(msg_ids=message_ids, min_length=3)
    print(f"Got {len(sentence_db)} sentences.")

    embeddings = _get_embeddings(
        sentence_ids=list(sentence_db.keys()), model_name=model_name
    )

    embeddings = _calc_pca(data=embeddings)

    _plot(embeddings=embeddings, sent_db=sentence_db)


def _get_relevant_message_ids() -> Set[int]:

    message_db = MessageDB.from_file(jsonl_path=jsonl_path)

    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_thread_responses(keep_op=True)
        .get_all_messages()
    )

    return {msg.msg_id for msg in practice_logs}


def _get_sentence_db(msg_ids: Set[int], min_length: int) -> Dict[str, Sentence]:

    sent_db_path = data_path.joinpath(f"sentences.pkl")
    print(f"Loading {sent_db_path} ...")

    with open(str(sent_db_path), "rb") as f:
        sent_db: Dict[str, Sentence] = pickle.load(f)

    sent_db = {
        k: v
        for k, v in sent_db.items()
        if v.msg_id in msg_ids and len(v.sentence.split()) >= min_length
    }
    return sent_db


def _get_embeddings(sentence_ids: List[str], model_name: str) -> np.ndarray:

    sent_emb_db_path = embeddings_path.joinpath(f"sent_embeddings_{model_name}.pkl")
    print(f"Loading {sent_emb_db_path} ...")

    with open(str(sent_emb_db_path), "rb") as f:
        sent_emb_db: Dict[str, np.ndarray] = pickle.load(f)

    print("Calculating embeddings ...")
    embeddings = np.vstack([sent_emb_db[sid] for sid in sentence_ids])

    return embeddings


def _calc_pca(data: np.ndarray, n_components=10) -> np.ndarray:
    pca = PCA(n_components=n_components)
    print(f"Training PCA on {data.shape[0]} embeddings ...")
    return pca.fit_transform(data)


def _create_embedding_dataframe(embeddings: np.ndarray, sent_db: Dict[str, Sentence]):

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        embeddings, columns=[f"PCA_{i}" for i in range(embeddings.shape[1])]
    )
    df["sentence"] = [wrap(sent_db[sid].sentence, width=80)[0] for sid in sent_db]
    df = df.drop_duplicates(subset=["sentence"])
    print(df)

    return df


def _plot(embeddings: np.ndarray, sent_db: Dict[str, Sentence]):

    df = _create_embedding_dataframe(embeddings=embeddings, sent_db=sent_db)

    fig = px.scatter(
        data_frame=df,
        x="PCA_0",
        y="PCA_1",
        hover_data=["sentence"],
    )

    num_bars = 20

    fig.show()

    for i, title in [
        (0, '"Recognition" vs "Sleepiness"'),
        (1, '"Noticing" vs ???'),
        (2, '"Consistent Practice" vs "Weirdness"'),
        (3, '"Challenge" vs "Enjoyment"'),
        (4, '"Investigation" vs "Happiness"'),
        (5, '"Mental Action" vs "Bodily Discomfort"'),
    ]:

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
                textfont=dict(size=18),
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
                textfont=dict(size=18, color="white"),
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
