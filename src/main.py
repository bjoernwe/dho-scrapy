from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.DhOSpider import DhOSpider, DhOCategory


def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DhOSpider, categories=[DhOCategory.DharmaDiagnostics])
    process.start()


if __name__ == '__main__':
    main()
