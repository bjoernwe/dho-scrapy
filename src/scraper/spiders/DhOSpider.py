import scrapy
from scrapy.http import HtmlResponse


class DhOSpider(scrapy.Spider):
    name = "dho"

    def start_requests(self):
        urls = [
            'https://www.dharmaoverground.org/discussion/-/message_boards/category/103268',  # Dharma Diagnostics
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):
        pass
