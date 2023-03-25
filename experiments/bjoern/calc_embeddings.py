import pickle
from typing import Dict
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from data_models.message_db import MessageDB
from experiments.utils.paths import default_embeddings_path
from experiments.utils.paths import default_jsonl_path


def main():

    model_names = [
        "all-mpnet-base-v2",
        "multi-qa-mpnet-base-dot-v1",
        "all-distilroberta-v1",
        "all-MiniLM-L12-v2",
        "multi-qa-distilbert-cos-v1",
        "all-MiniLM-L6-v2",
        "multi-qa-MiniLM-L6-cos-v1",
        "paraphrase-multilingual-mpnet-base-v2",
        "paraphrase-albert-small-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
        "paraphrase-MiniLM-L3-v2",
        "distiluse-base-multilingual-cased-v1",
        "distiluse-base-multilingual-cased-v2",
    ]

    calc_and_store_embeddings(model_names=model_names)


def calc_and_store_embeddings(model_names: List[str]):

    message_db = MessageDB.from_file(jsonl_path=default_jsonl_path)

    for model_name in model_names:

        msg_embeddings = calc_embeddings(db=message_db, model_name=model_name)
        out_path = default_embeddings_path.joinpath(f"embeddings_{model_name}.pkl")

        with open(str(out_path), "wb") as f:
            pickle.dump(msg_embeddings, f)

        print(f"Saved: {out_path}")


def calc_embeddings(db: MessageDB, model_name: str) -> Dict[int, np.ndarray]:
    """
    Calculate embeddings (based on the message body) for all messages in MessageDB and store them in a
    dictionary (msg_id -> embedding-vector).
    """

    model = SentenceTransformer(model_name)
    msg_embeddings: Dict[int, np.ndarray] = {}

    print(f"Calculating embeddings for {len(db)} messages ...")

    for msg in tqdm(db.get_all_messages()):
        msg_emb = model.encode([msg.msg])
        msg_embeddings[msg.msg_id] = msg_emb

    return msg_embeddings


if __name__ == "__main__":
    main()
