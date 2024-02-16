from typing import Iterator
from typing import List
from typing import Optional

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from scrapy.http import XmlResponse

from data_model.forum_message import ForumMessage
from scraper.spiders.dho.categories import DhOCategory


class DhOSpider(scrapy.Spider):

    name = "dho"

    def __init__(self, categories: Optional[List[DhOCategory]] = None, **kwargs):
        super().__init__(**kwargs)
        self._categories = categories or [DhOCategory.DharmaDiagnostics]

    def start_requests(self):
        yield from self._request_categories(categories=self._categories)

    def _request_categories(
        self, categories: List[DhOCategory]
    ) -> Iterator[scrapy.Request]:
        for category in categories:
            url = str(category.value)
            yield scrapy.Request(
                url=url, callback=self.parse, cb_kwargs={"category": category}
            )

    def parse(self, response: HtmlResponse, **kwargs):

        try:
            category = kwargs["category"]
        except KeyError:
            raise CloseSpider("Current category should be known but isn't!")

        yield from self._request_thread_messages(response=response, category=category)
        yield from self._request_other_pages(response=response, category=category)

    @classmethod
    def _request_thread_messages(
        cls, response: HtmlResponse, category: DhOCategory
    ) -> Iterator[scrapy.Request]:
        for thread_url in cls._extract_thread_rss_urls(response=response):
            yield scrapy.Request(
                thread_url,
                callback=cls._extract_messages_from_rss,
                cb_kwargs={"category": category},
            )

    def _request_other_pages(
        self, response: HtmlResponse, category: DhOCategory
    ) -> Iterator[scrapy.Request]:
        for next_page_url in self._extract_other_page_urls(response):
            yield scrapy.Request(
                next_page_url, callback=self.parse, cb_kwargs={"category": category}
            )

    @staticmethod
    def _extract_messages_from_rss(
        response: XmlResponse, category: DhOCategory
    ) -> Iterator[ForumMessage]:
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

    @staticmethod
    def _extract_thread_rss_urls(response: HtmlResponse) -> List[str]:
        thread_urls = response.xpath(
            '//a[contains(@role, "menuitem") and contains(@href, "threadId=")]/@href'
        ).getall()
        thread_urls = [
            thread_url.replace("&max=100&", "&max=1000&") for thread_url in thread_urls
        ]
        return thread_urls

    @classmethod
    def _extract_other_page_urls(cls, response: HtmlResponse) -> List[str]:
        next_page_urls = response.xpath(
            '//ul[contains(@class, "pagination")]/li[not(contains(@class, "inactive"))]/a/@href'
        ).getall()
        next_page_urls = [url for url in next_page_urls if cls._is_valid_url(url)]
        return next_page_urls

    @staticmethod
    def _is_valid_url(url: str) -> bool:

        if not url:
            return False

        if not url.startswith("http"):
            return False

        return True
