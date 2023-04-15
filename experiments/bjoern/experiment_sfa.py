from textwrap import wrap

import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sksfa import SFA

from data_tools.dho_categories import DhOCategory
from experiments.experiment_setup import ExperimentSetup


def main():

    author = "curious-frame"
    sentences_per_snippet = 3
    # model_name = "paraphrase-albert-small-v2"
    # model_name = "multi-qa-mpnet-base-dot-v1"
    model_name = "paraphrase-MiniLM-L3-v2"

    plot_sfa(
        author=author,
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
        show_plot=True,
    )


def plot_sfa(
    author: str, model_name: str, sentences_per_snippet: int, show_plot: bool = True
):

    experiment = ExperimentSetup(
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
    )

    # Load practice logs of a certain user
    snippets = (
        experiment.message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_snippets(sentences_per_snippet=sentences_per_snippet)
    )
    texts = [snippet.text for snippet in snippets]

    # Load & calc embeddings
    embeddings = experiment.embedder.get_embeddings(texts=texts)

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
    df["msg_id"] = [snippet.source_msg_id for snippet in snippets]
    df["date"] = [
        experiment.message_db[snippet.source_msg_id].date for snippet in snippets
    ]
    df["text"] = ["<br>".join(wrap(snippet.text, width=100)) for snippet in snippets]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df["date"],
        y=df["SFA_0"],
        title=f"SFA on Embedded Messages (Author: {author} / Model: {model_name})",
        hover_data=["msg_id", "text"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
