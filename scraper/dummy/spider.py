from collections import defaultdict
from datetime import datetime
from pathlib import Path

import scrapy
from scrapy.http import HtmlResponse

from data_tools.dho_message import ForumMessage
from scraper.dummy.categories import DummyCategory


class DummySpider(scrapy.Spider):

    name = "dummy"
    custom_settings = defaultdict(dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def set_output_feed(cls, jsonlines_path: Path):
        jsonlines_uri: str = (
            jsonlines_path.absolute().as_uri()
        )  # Add file:// scheme to work on Windows
        cls.custom_settings["FEEDS"][jsonlines_uri] = {"format": "jsonlines"}

    def start_requests(self):
        urls = ["http://www.google.com"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):
        yield ForumMessage(
            msg_id=0,
            thread_id=0,
            date=datetime.now(),
            is_first_in_thread=True,
            category=DummyCategory.DefaultCategory,
            author="someone",
            title="Dummy Message",
            msg="foo bar",
        )
