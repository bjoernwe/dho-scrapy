from typing import List
from typing import Optional

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


class RedditSpider(scrapy.Spider):

    name = "reddit"

    def __init__(self, subreddits: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        # https://docs.scrapy.org/en/latest/intro/tutorial.html
        # or look at DhOSpider

    def start_requests(self):
        pass

    def parse(self, response: HtmlResponse, **kwargs):
        pass


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(RedditSpider, subreddits=["streamentry"])
    process.start()
