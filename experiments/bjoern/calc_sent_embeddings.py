import pickle
from pathlib import Path
from typing import Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from data_models.sentence import Sentence
from experiments.utils.paths import data_path
from experiments.utils.paths import embeddings_path


def main():

    model_name = "paraphrase-albert-small-v2"
    sentences_path = data_path.joinpath("sentences.pkl")
    sent_embeddings_path = embeddings_path.joinpath(f"sent_embeddings_{model_name}.pkl")

    with open(str(sentences_path), "rb") as f:
        sentences = pickle.load(f)

    _calc_and_store_sent_embeddings(
        sentences=sentences,
        model_name=model_name,
        out_path=sent_embeddings_path,
    )


def _calc_and_store_sent_embeddings(
    sentences: Dict[str, Sentence], model_name: str, out_path: Path
):

    if out_path.exists():
        with open(str(out_path), "rb") as f:
            sent_embeddings = pickle.load(f)
    else:
        sent_embeddings = {}

    try:
        sent_embeddings = _update_sent_embeddings(
            sent_embeddings=sent_embeddings,
            sentences=sentences,
            model_name=model_name,
        )
    except KeyboardInterrupt:
        pass

    with open(str(out_path), "wb") as f:
        pickle.dump(sent_embeddings, f)

    print(f"Saved: {out_path}")


def _update_sent_embeddings(
    sent_embeddings: Dict[str, np.ndarray],
    sentences: Dict[str, Sentence],
    model_name: str,
) -> Dict[str, np.ndarray]:

    model = SentenceTransformer(model_name)

    print(f"Calculating embeddings for {len(sentences)} sentences ...")

    for sid, sent in tqdm(sentences.items()):
        if sid in sent_embeddings:
            continue
        sent_emb = model.encode([sent.sentence])
        sent_embeddings[sid] = sent_emb

    return sent_embeddings


if __name__ == "__main__":
    main()
