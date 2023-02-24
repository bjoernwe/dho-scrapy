from datetime import datetime
from typing import List

import nltk
from pydantic import BaseModel
from pydantic import validator

from data_models.categories import DhOCategory
from data_models.sentence import Sentence


class DhOMessage(BaseModel):

    msg_id: int
    thread_id: int
    date: datetime
    is_first_in_thread: bool
    category: DhOCategory
    author: str
    title: str
    msg: str

    @validator("date", pre=True)
    def dho_date_to_datetime(cls, dt) -> datetime:

        if type(dt) is datetime:
            return dt

        try:
            return datetime.fromisoformat(dt)
        except ValueError:
            pass

        return datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S %Z")

    @property
    def sentences(self) -> List[Sentence]:

        nltk.download("punkt", quiet=True)

        sentences = [
            Sentence(msg_id=self.msg_id, sentence_idx=i, sentence=snt)
            for i, snt in enumerate(nltk.sent_tokenize(text=self.msg))
        ]

        return sentences
