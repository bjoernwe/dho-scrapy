import hashlib

from pydantic import BaseModel


class TextSnippet(BaseModel):

    source_msg_id: int
    text: str

    class Config:
        frozen = True

    def __add__(self, other: "TextSnippet"):
        assert other.source_msg_id == self.source_msg_id
        return TextSnippet(
            source_msg_id=self.source_msg_id,
            text=self.text + " " + other.text,
        )

    @property
    def sid(self) -> str:
        key = (
            str(self.source_msg_id).encode("UTF-8"),
            self.text.encode("UTF-8"),
        )
        sha = hashlib.sha1()
        for k in key:
            sha.update(k)
        return sha.hexdigest()[:10]
