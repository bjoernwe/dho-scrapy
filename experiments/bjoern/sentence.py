import hashlib

from pydantic import BaseModel


class Sentence(BaseModel):

    msg_id: int
    sentence: str

    @property
    def sid(self) -> str:
        key = (
            str(self.msg_id).encode("UTF-8"),
            self.sentence.encode("UTF-8"),
        )
        sha = hashlib.sha1()
        for k in key:
            sha.update(k)
        return sha.hexdigest()[:10]
