from pathlib import Path
from typing import Optional

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dho_scraper.dho_spider import DhOSpider, DhOCategory


def main(output_file: Optional[str] = None):

    if output_file:
        DhOSpider.set_output_feed(jsonlines_path=output_file)

    process = CrawlerProcess(get_project_settings())
    process.crawl(DhOSpider, categories=[DhOCategory.DharmaDiagnostics])
    process.start()


if __name__ == '__main__':

    output_file = './output/items.jsonl'
    project_root = Path(__file__).parent.parent

    main(output_file=str(project_root.joinpath(output_file)))
