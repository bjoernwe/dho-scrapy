from textwrap import wrap

import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from data_tools.dho_categories import DhOCategory
from experiments.experiment_setup import ExperimentSetup


def main():

    author = "curious-frame"
    sentences_per_snippet = 3
    # model_name = "paraphrase-albert-small-v2"
    # model_name = "multi-qa-mpnet-base-dot-v1"
    model_name = "paraphrase-MiniLM-L3-v2"

    plot_pca(
        author=author,
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
        show_plot=True,
    )


def plot_pca(
    author: str, model_name: str, sentences_per_snippet: int = 0, show_plot: bool = True
):

    experiment = ExperimentSetup(
        model_name=model_name,
        sentences_per_snippet=sentences_per_snippet,
    )

    # Load practice logs from a certain user
    snippets = (
        experiment.message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .get_snippets(sentences_per_snippet=sentences_per_snippet)
    )

    # Calc PCA
    pca = PCA(n_components=10)
    texts = [snippet.text for snippet in snippets]
    embeddings = experiment.embedder.get_embeddings(texts=texts)
    pca_data = pca.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    column_names = [f"PCA_{i}" for i in range(pca_data.shape[1])]
    df = pd.DataFrame(pca_data, columns=column_names)
    df["msg_id"] = [snippet.source_msg_id for snippet in snippets]
    df["text"] = ["<br>".join(wrap(snippet.text, width=100)) for snippet in snippets]
    print(df)

    # Plot
    fig = px.scatter(
        data_frame=df,
        x=df.columns[0],
        y=df.columns[1],
        title=f"Text Embedding (Model: {model_name})",
        hover_data=["msg_id", "text"],
    )
    if show_plot:
        fig.show()


if __name__ == "__main__":
    main()
