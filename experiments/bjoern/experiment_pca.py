from textwrap import wrap
from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pandas import DataFrame
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA

from data_tools.textsnippet import TextSnippet
from experiments.experiment_setup import ExperimentSetup
from scraper.dho_scraper.categories import DhOCategory


def main():

    model_name = "paraphrase-albert-small-v2"
    sentences_per_snippet = 3

    _plot_sentence_pca(
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
    )


def _plot_sentence_pca(model_name: str, sentences_per_snippet: int = 0):

    experiment = ExperimentSetup(
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
    )

    snippets = _get_text_snippets(experiment=experiment)
    print(f"Got {len(snippets)} messages.")
    texts = [snippet.text for snippet in snippets]

    embeddings = experiment.embedder.get_embeddings(texts=texts)
    embeddings = PCA(n_components=10).fit_transform(embeddings)

    df = _create_embedding_dataframe(embeddings=embeddings, texts=texts)
    _plot(df=df)


def _get_text_snippets(experiment: ExperimentSetup) -> List[TextSnippet]:
    return (
        experiment.message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_thread_responses(keep_op=True)
        .filter_message_length(min_num_words=1)
        .get_snippets(sentences_per_snippet=experiment.sentences_per_snippet)
    )


def _create_embedding_dataframe(embeddings: np.ndarray, texts: List[str]):

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        embeddings, columns=[f"PCA_{i}" for i in range(embeddings.shape[1])]
    )
    df["text"] = [wrap(text, width=80)[0] for text in texts]
    df["full_text"] = ["<br>".join(wrap(text, width=80)) for text in texts]
    df = df.drop_duplicates(subset=["text"])
    print(df)

    return df


def _plot(df: DataFrame):

    fig = px.scatter(
        data_frame=df,
        x="PCA_0",
        y="PCA_1",
        hover_data=["text"],
    )

    fig.show()

    num_bars = 20

    for i, title in [
        (0, "??? vs ???"),
        (1, "??? vs ???"),
        (2, "??? vs ???"),
        (3, "??? vs ???"),
        (4, "??? vs ???"),
        (5, "??? vs ???"),
    ]:

        df = df.sort_values(f"PCA_{i}")

        fig = make_subplots(
            rows=1, cols=2, subplot_titles=["extremes (-)", "extremes (+)"]
        )

        fig.add_trace(
            go.Bar(
                x=df[::-1][f"PCA_{i}"][-num_bars:],
                text=df[::-1]["text"][-num_bars:],
                hovertext=df[::-1]["full_text"][-num_bars:],
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
                text=df["text"][-num_bars:],
                hovertext=df["full_text"][-num_bars:],
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
