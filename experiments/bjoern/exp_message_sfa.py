from textwrap import wrap

import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sksfa import SFA

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

    plot_sfa(author=author, model_name=model_name, show_plot=True)


def plot_sfa(author: str, model_name: str, show_plot: bool = True):

    # Load practice logs of a certain user
    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    text_snippets = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_snippets(sentences_per_snippet=0)
    )

    # Load & calc embeddings
    shelf_path = default_embeddings_path.joinpath(f"msg_emb_{model_name}.shelf")
    embeddings_db = EmbeddingsDB(shelf_path=shelf_path)
    embeddings = embeddings_db.get_embeddings(text_snippets=text_snippets)

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
    df["msg_id"] = [snippet.source_msg_id for snippet in text_snippets]
    df["date"] = [message_db[snippet.source_msg_id].date for snippet in text_snippets]
    df["msg"] = [
        "<br>".join(wrap(snippet.text, width=100)) for snippet in text_snippets
    ]
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
