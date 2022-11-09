import logging

from pathlib import Path
from typing import Optional

import typer

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dho_scraper.dho_spider import DhOSpider, DhOCategory


def crawl_messages(out_file: Optional[str] = None):

    if not out_file:
        out_file = Path(__file__).parent.parent.joinpath('data/messages.jsonl')

    logging.info(f'Writing DhO messages to {out_file} ...')
    DhOSpider.set_output_feed(jsonlines_path=out_file)

    process = CrawlerProcess(get_project_settings())
    process.crawl(DhOSpider, categories=[DhOCategory.DharmaDiagnostics])
    process.start()


if __name__ == '__main__':
    typer.run(crawl_messages)
