import hashlib

from pydantic import BaseModel


class Sentence(BaseModel):

    msg_id: int
    sentence_idx: int
    sentence: str

    class Config:
        frozen = True

    @property
    def sid(self) -> str:
        return str(self.__hash__())
