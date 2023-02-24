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
        key = (
            str(self.msg_id).encode("UTF-8"),
            str(self.sentence_idx).encode("UTF-8"),
            self.sentence.encode("UTF-8"),
        )
        sha = hashlib.sha1()
        for k in key:
            sha.update(k)
        return sha.hexdigest()[:10]
