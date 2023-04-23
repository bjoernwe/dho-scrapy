from collections import defaultdict
from pathlib import Path
from typing import List
from typing import Optional

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from scrapy.http import XmlResponse

from data_tools.dho_message import ForumMessage
from scraper.dho_scraper.categories import DhOCategory


class DhOSpider(scrapy.Spider):

    name = "dho"
    custom_settings = defaultdict(dict)

    def __init__(self, categories: Optional[List[DhOCategory]] = None, **kwargs):
        super().__init__(**kwargs)
        self._categories = categories or [DhOCategory.DharmaDiagnostics]

    @classmethod
    def set_output_feed(cls, jsonlines_path: Path):
        jsonlines_uri: str = (
            jsonlines_path.absolute().as_uri()
        )  # Add file:// scheme to work on Windows
        cls.custom_settings["FEEDS"][jsonlines_uri] = {"format": "jsonlines"}

    def start_requests(self):
        for category in self._categories:
            url = str(category.value)
            yield scrapy.Request(
                url=url, callback=self.parse, cb_kwargs={"category": category}
            )

    def parse(self, response: HtmlResponse, **kwargs):

        try:
            category = kwargs["category"]
        except KeyError:
            raise CloseSpider("Current category should be known but isn't!")

        for thread_url in _get_thread_rss_urls(response):
            yield scrapy.Request(
                thread_url,
                callback=_get_messages_from_rss,
                cb_kwargs={"category": category},
            )

        for next_page_url in _get_other_page_urls(response):
            yield scrapy.Request(
                next_page_url, callback=self.parse, cb_kwargs={"category": category}
            )


def _get_messages_from_rss(
    response: XmlResponse, category: DhOCategory
) -> List[ForumMessage]:
    for i, item in enumerate(reversed(response.xpath("//item"))):
        item.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
        message = ForumMessage(
            msg_id=item.xpath("./link/text()").get().split("=")[-1],
            category=category,
            thread_id=response.xpath("./channel/link/text()").get().split("=")[-1],
            title=item.xpath("./title/text()").get(),
            author=item.xpath("./dc:creator/text()").get(),
            date=item.xpath("./pubDate/text()").get(),
            msg=item.xpath("./description/text()").get(),
            is_first_in_thread=(i == 0),
        )
        yield message


def _get_thread_rss_urls(response: HtmlResponse) -> List[str]:
    thread_urls = response.xpath(
        '//a[contains(@role, "menuitem") and contains(@href, "threadId=")]/@href'
    ).getall()
    for thread_url in thread_urls:
        thread_url.replace("&max=100&", "&max=1000&")
        yield thread_url


def _get_other_page_urls(response: HtmlResponse) -> List[str]:
    next_page_urls = response.xpath(
        '//ul[contains(@class, "pagination")]/li[not(contains(@class, "inactive"))]/a/@href'
    ).getall()
    next_page_urls = [url for url in next_page_urls if _is_valid_url(url)]
    return next_page_urls


def _is_valid_url(url: str) -> bool:

    if not url:
        return False

    if not url.startswith("http"):
        return False

    return True
