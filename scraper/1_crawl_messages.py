import logging
from pathlib import Path
from typing import Optional

import typer
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from data_models.categories import DhOCategory
from scraper.dho_scraper.spider import DhOSpider


def crawl_messages(out_file: Optional[str] = None, overwrite_old: bool = True):
    """
    Crawl messages from Dharma Overground and store them into a JSONL file.

    :param out_file: JSONL file to store message to
    :param overwrite_old: Whether a previous JSONL file is overwritten
    """

    if not out_file:
        out_file = Path(__file__).parent.parent.joinpath("data/messages.jsonl")

    if overwrite_old:
        logging.info(f"Deleting old file {out_file}")
        out_file.unlink(missing_ok=True)

    logging.info(f"Writing DhO messages to {out_file} ...")
    DhOSpider.set_output_feed(jsonlines_path=out_file)

    process = CrawlerProcess(get_project_settings())
    process.crawl(
        DhOSpider, categories=[DhOCategory.PracticeLogs, DhOCategory.DharmaDiagnostics]
    )
    process.start()


if __name__ == "__main__":
    typer.run(crawl_messages)
