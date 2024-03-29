import logging

import typer
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.dho.categories import DhOCategory
from scraper.spiders.dho.spider import DhOSpider
from scraper.spiders.dummy.spider import DummySpider


def crawl_messages():
    """
    Run spiders to crawl messages.
    """

    logging.getLogger().addHandler(logging.StreamHandler())

    process = CrawlerProcess(get_project_settings())

    process.crawl(DummySpider)

    process.crawl(
        DhOSpider, categories=[DhOCategory.PracticeLogs, DhOCategory.DharmaDiagnostics]
    )

    process.start()


if __name__ == "__main__":
    typer.run(crawl_messages)
