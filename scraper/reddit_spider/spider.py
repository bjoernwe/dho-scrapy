from collections import defaultdict
from pathlib import Path
from typing import List
from typing import Optional

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

from data_models.dho_message import DhOMessage
from scraper.reddit_spider.settings import RedditSettings


class RedditSpider(scrapy.Spider):

    name = "reddit"
    custom_settings = defaultdict(dict)

    def __init__(self, subreddits: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        self._subreddits = subreddits or ["streamentry"]
        self._headers = self._get_auth_headers()

    @classmethod
    def set_output_feed(cls, jsonlines_path: Path):
        jsonlines_uri: str = (
            jsonlines_path.absolute().as_uri()
        )  # Add file:// scheme to work on Windows
        cls.custom_settings["FEEDS"][jsonlines_uri] = {"format": "jsonlines"}

    def start_requests(self):
        for subreddit in self._subreddits:
            url = f"https://oauth.reddit.com/r/{subreddit}/hot"
            yield scrapy.Request(url=url, callback=self.parse, headers=self._headers)

    def parse(self, response: HtmlResponse, **kwargs) -> DhOMessage:
        data = response.json()
        print(data)
        # TODO Return a DhOMessage object
        return DhOMessage()

    @staticmethod
    def _get_auth_headers() -> dict:

        settings = RedditSettings()

        auth = requests.auth.HTTPBasicAuth(
            settings.reddit_public_id, settings.reddit_secret
        )
        data = {
            "grant_type": "password",
            "username": settings.reddit_username,
            "password": settings.reddit_password,
        }
        headers = {"User-Agent": "RedditSpider/0.0.1"}

        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
        )

        token = res.json()["access_token"]
        headers["Authorization"] = f"bearer {token}"

        return headers


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(RedditSpider, subreddits=["streamentry"])
    process.start()
