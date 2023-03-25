import pickle
from pathlib import Path
from typing import Dict

import nltk
from tqdm import tqdm

from data_models.message_db import MessageDB
from data_models.sentence import Sentence
from experiments.utils.paths import data_path
from experiments.utils.paths import default_jsonl_path


def main():
    msg_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    out_path = data_path.joinpath("sentences.pkl")
    calc_and_store_sentences(msg_db=msg_db, out_path=out_path)


def calc_and_store_sentences(msg_db: MessageDB, out_path: Path):

    sentences = calc_sentences(msg_db=msg_db)

    with open(str(out_path), "wb") as f:
        pickle.dump(sentences, f)

    print(f"Saved: {out_path}")


def calc_sentences(msg_db: MessageDB) -> Dict[str, Sentence]:

    nltk.download("punkt")  # Dependency of the sentence tokenizer
    sentences: Dict[str, Sentence] = {}

    for msg in tqdm(msg_db.get_all_messages()):
        for i, sntc_txt in enumerate(nltk.sent_tokenize(text=msg.msg)):
            sentence = Sentence(msg_id=msg.msg_id, sentence_idx=i, sentence=sntc_txt)
            sentences[sentence.sid] = sentence

    return sentences


if __name__ == "__main__":
    main()
