from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.DhOSpider import DhOSpider


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DhOSpider)
    process.start()


if __name__ == '__main__':
    main()
