from pydantic import BaseSettings


class ScrapySettings(BaseSettings):

    reddit_public_id: str
    reddit_secret: str
    reddit_username: str
    reddit_password: str

    class Config:
        env_file = ".env"
        env_prefix = "scrapy_"
