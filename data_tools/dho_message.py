from datetime import datetime
from typing import List

import nltk
from pydantic import BaseModel
from pydantic import validator

from data_tools.textsnippet import TextSnippet


class ForumMessage(BaseModel):

    msg_id: int
    thread_id: int
    date: datetime
    is_first_in_thread: bool
    category: str
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
    def sentences(self) -> List[TextSnippet]:

        nltk.download("punkt", quiet=True)

        sentences = [
            TextSnippet(source_msg_id=self.msg_id, text=snt)
            for i, snt in enumerate(nltk.sent_tokenize(text=self.msg))
        ]

        return sentences

    def get_snippets(self, sentences_per_snippet: int = 1) -> List[TextSnippet]:

        if not sentences_per_snippet:
            snippet_with_full_message = TextSnippet(
                source_msg_id=self.msg_id, text=self.msg
            )
            return [snippet_with_full_message]

        sentences = self.sentences

        if not sentences:
            return []

        if sentences_per_snippet > 1:
            windows = [
                sentences[i : i + sentences_per_snippet]
                for i in range(max(0, len(sentences) - sentences_per_snippet) + 1)
            ]
            sentences = [sum(window[1:], start=window[0]) for window in windows]

        return sentences
