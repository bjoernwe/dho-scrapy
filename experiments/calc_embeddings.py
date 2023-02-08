import pickle
from typing import Dict
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from experiments.utils.paths import jsonl_path
from experiments.utils.paths import model_path
from message_db.message_db import MessageDB


def calc_and_store_embeddings(model_names: List[str]):

    for model_name in model_names:

        db = MessageDB.from_file(jsonl_path=jsonl_path)
        msg_embeddings = calc_embeddings(db=db, model_name=model_name)

        out_path = model_path.joinpath(f"embeddings_{model_name}.pkl")
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

    model_names = [
        "all-MiniLM-L12-v2",
        "multi-qa-mpnet-base-dot-v1",
    ]

    calc_and_store_embeddings(model_names=model_names)
