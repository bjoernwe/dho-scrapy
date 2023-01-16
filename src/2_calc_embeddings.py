import numpy as np
import pickle

from pathlib import Path
from typing import List, Dict

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from dho_scraper.items import DhOMessage
from message_db.message_db import MessageDB


def calc_embeddings(jsonl_path: Path, out_path: Path):
    """
    Calculate embeddings (based on the message body) for all messages in jsonl_path and store them in a
    dictionary (msg_id -> embedding-vector).
    """

    db = MessageDB.from_file(jsonl_path=jsonl_path)
    model = SentenceTransformer('all-MiniLM-L12-v2')

    msg_embeddings: Dict[int, np.ndarray] = {}

    print(f'Calculating embeddings for {len(db)} messages ...')

    for msg in tqdm(db.get_all_messages()):
        msg_emb = model.encode([msg.msg])[0,:]
        assert msg_emb.ndim == 1
        assert msg_emb.shape[0] == 384
        msg_embeddings[msg.msg_id] = msg_emb

    with open(str(out_path), 'wb') as f:
        pickle.dump(msg_embeddings, f)
    print(f'Saved: {out_path}')


if __name__ == '__main__':

    data_path = Path(__file__).parent.parent.joinpath('data')
    jsonl_path = data_path.joinpath('messages.jsonl')
    out_path = data_path.joinpath('embeddings.pkl')

    calc_embeddings(jsonl_path=jsonl_path, out_path=out_path)
