from collections import defaultdict
from enum import Enum
from typing import List, Optional

import scrapy

from scrapy.http import HtmlResponse, XmlResponse
from dho_scraper.items import DhOMessage


class DhOCategory(str, Enum):
    ContemporaryBuddhism = 'https://www.dharmaoverground.org/discussion/-/message_boards/category/13969849'
    DharmaDiagnostics = 'https://www.dharmaoverground.org/discussion/-/message_boards/category/103268'
    PracticeLogs = 'https://www.dharmaoverground.org/discussion/-/message_boards/category/2658626'


class DhOSpider(scrapy.Spider):

    name = "dho"
    custom_settings = defaultdict(dict)

    def __init__(self, categories: Optional[List[DhOCategory]] = None, **kwargs):
        super().__init__(**kwargs)
        self._categories = categories or [DhOCategory.DharmaDiagnostics]

    @classmethod
    def set_output_feed(cls, jsonlines_path: str):
        cls.custom_settings['FEEDS'][jsonlines_path] = {'format': 'jsonlines'}

    def start_requests(self):
        urls = [str(category.value) for category in self._categories]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):

        for thread_url in _get_thread_rss_urls(response):
            yield scrapy.Request(thread_url, callback=_get_messages_from_rss)

        for next_page_url in _get_other_page_urls(response):
            yield scrapy.Request(next_page_url, callback=self.parse)


def _get_messages_from_rss(response: XmlResponse, **_) -> List[DhOMessage]:
    for i, item in enumerate(reversed(response.xpath('//item'))):
        item.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
        message = DhOMessage(
            msg_id=item.xpath('./link/text()').get().split('=')[-1],
            thread_id=response.xpath('./channel/link/text()').get().split('=')[-1],
            title=item.xpath('./title/text()').get(),
            author=item.xpath('./dc:creator/text()').get(),
            date=item.xpath('./pubDate/text()').get(),
            msg=item.xpath('./description/text()').get(),
            is_first_in_thread=(i==0),
        )
        yield message


def _get_thread_rss_urls(response: HtmlResponse) -> List[str]:
    thread_urls = response.xpath('//a[contains(@role, "menuitem") and contains(@href, "threadId=")]/@href').getall()
    for thread_url in thread_urls:
        thread_url.replace('&max=100&', '&max=1000&')
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

    if not url.startswith('http'):
        return False

    return True
