import pickle
from pathlib import Path
from typing import Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from message_db.message_db import MessageDB


def calc_embeddings(jsonl_path: Path, out_path: Path):
    """
    Calculate embeddings (based on the message body) for all messages in jsonl_path and store them in a
    dictionary (msg_id -> embedding-vector).
    """

    db = MessageDB.from_file(jsonl_path=jsonl_path)
    model = SentenceTransformer("all-MiniLM-L12-v2")

    msg_embeddings: Dict[int, np.ndarray] = {}

    print(f"Calculating embeddings for {len(db)} messages ...")

    for msg in tqdm(db.get_all_messages()):
        msg_emb = model.encode([msg.msg])
        assert msg_emb.shape == (1, 384)
        msg_embeddings[msg.msg_id] = msg_emb

    with open(str(out_path), "wb") as f:
        pickle.dump(msg_embeddings, f)
    print(f"Saved: {out_path}")


if __name__ == "__main__":

    # model_name = "all-MiniLM-L12-v2"
    model_name = "multi-qa-mpnet-base-dot-v1"

    data_path = Path(__file__).parent.parent.joinpath("data")
    jsonl_path = data_path.joinpath("messages.jsonl")
    out_path = data_path.joinpath(f"embeddings_{model_name}.pkl")

    calc_embeddings(jsonl_path=jsonl_path, out_path=out_path)
