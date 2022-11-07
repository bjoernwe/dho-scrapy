from typing import List

import scrapy

from scrapy.http import HtmlResponse, XmlResponse
from scraper.items import DhOMessage


class DhOSpider(scrapy.Spider):
    name = "dho"

    def start_requests(self):
        urls = [
            # Dharma Diagnostics
            'https://www.dharmaoverground.org/discussion/-/message_boards/category/103268?_com_liferay_message_boards_web_portlet_MBPortlet_delta2=20&_com_liferay_message_boards_web_portlet_MBPortlet_orderByCol=modified-date&_com_liferay_message_boards_web_portlet_MBPortlet_orderByType=desc&_com_liferay_message_boards_web_portlet_MBPortlet_resetCur=false&_com_liferay_message_boards_web_portlet_MBPortlet_cur2=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):

        for thread_url in _get_thread_rss_urls(response):
            yield scrapy.Request(thread_url, callback=_get_messages_from_rss)

        for next_page_url in _get_other_page_urls(response):
            yield scrapy.Request(next_page_url, callback=self.parse)


def _get_messages_from_rss(response: XmlResponse, **kwargs) -> List[DhOMessage]:
    for item in response.xpath('//item'):
        yield DhOMessage(
            title=item.xpath('./title/text()').get(),
        )


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
