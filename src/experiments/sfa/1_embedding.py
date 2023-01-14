import numpy as np

from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer

from dho_scraper.items import DhOMessage
from message_db.message_db import MessageDB


def main(jsonl_path: Path, out_path: Path):

    msgs = _read_messages(jsonl_path=jsonl_path)
    strs = _get_message_bodies(msgs=msgs)
    embeddings = _calc_embeddings(strs=strs)

    np.save(str(out_path), embeddings)
    print(f'Saved: {out_path}')


def _read_messages(jsonl_path: Path) -> List[DhOMessage]:
    db = MessageDB.from_file(jsonl_path=jsonl_path)
    return db.get_all_messages()


def _get_message_bodies(msgs: List[DhOMessage]) -> List[str]:
    return [msg.msg for msg in msgs]


def _calc_embeddings(strs: List[str]) -> np.ndarray:
    model = SentenceTransformer('all-MiniLM-L12-v2')
    print(f'Calculating embeddings for {len(strs)} messages ...')
    return model.encode(strs, convert_to_numpy=True)


if __name__ == '__main__':

    jsonl_path = Path(__file__).parent.parent.parent.parent.joinpath('data/messages.jsonl')
    out_path = Path(__file__).parent.joinpath('1_embeddings.npy')

    main(jsonl_path=jsonl_path, out_path=out_path)
