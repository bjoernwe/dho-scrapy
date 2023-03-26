from textwrap import wrap

import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA

from data_tools.default_paths import default_embeddings_path
from data_tools.default_paths import default_jsonl_path
from data_tools.dho_categories import DhOCategory
from data_tools.embeddings_db import EmbeddingsDB
from data_tools.message_db import MessageDB


def main():

    author = "curious-frame"
    model_name = "paraphrase-albert-small-v2"
    # model_name = "multi-qa-mpnet-base-dot-v1"
    # model_name = "paraphrase-MiniLM-L3-v2"

    plot_pca(author=author, model_name=model_name, show_plot=True)


def plot_pca(author: str, model_name: str, show_plot: bool = True):

    # Load practice logs of a certain user
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    text_snippets = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_snippets(sentences_per_snippet=0)
    )

    # Load embeddings
    shelf_path = default_embeddings_path.joinpath(f"msg_emb_{model_name}.shelf")
    embeddings = EmbeddingsDB(shelf_path=shelf_path)

    # Calc PCA
    pca = PCA(n_components=10)
    embeddings = embeddings.get_embeddings(text_snippets=text_snippets)
    components = pca.fit_transform(embeddings)

    # Create DataFrame with embeddings and message texts
    df = pd.DataFrame(
        components, columns=[f"PCA_{i}" for i in range(components.shape[1])]
    )
    df["msg_id"] = [snippet.source_msg_id for snippet in text_snippets]
    df["msg"] = [
        "<br>".join(wrap(snippet.text, width=100)) for snippet in text_snippets
    ]
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
