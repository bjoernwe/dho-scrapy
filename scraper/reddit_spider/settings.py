from pydantic import BaseSettings


class RedditSettings(BaseSettings):

    reddit_public_id: str
    reddit_secret: str
    reddit_username: str
    reddit_password: str

    class Config:
        env_file = "reddit_spider/.env"
        env_prefix = "scrapy_"
