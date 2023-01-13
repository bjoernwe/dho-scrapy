from pathlib import Path
from typing import List

import pytest

from _pytest.tmpdir import TempPathFactory
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dho_scraper.categories import DhOCategory
from dho_scraper.items import DhOMessage
from dho_scraper.spider import DhOSpider


@pytest.fixture(scope='session')
def session_tmp_path(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp('dho-scraper')


@pytest.fixture(scope='session')
def test_dho_category() -> DhOCategory:
    return DhOCategory.ContemporaryBuddhism


@pytest.fixture(scope='session')
def jsonl_path(session_tmp_path: Path, test_dho_category: DhOCategory) -> Path:

    jsonl_out_path = session_tmp_path.joinpath('items.jsonl')

    settings = get_project_settings()
    settings['FEEDS'][str(jsonl_out_path)] = {'format': 'jsonlines'}
    settings['PIPELINE_MIN_MESSAGE_WORDS'] = 1

    process = CrawlerProcess(settings=settings)
    process.crawl(DhOSpider, categories=[test_dho_category])
    process.start()

    return jsonl_out_path


@pytest.fixture(scope='session')
def crawled_messages(jsonl_path: Path) -> List[DhOMessage]:
    return _messages_from_file(jsonl_path)


def _messages_from_file(jsonl_path: Path) -> List[DhOMessage]:

    messages = []

    with open(str(jsonl_path), 'r') as file:
        for line in file.readlines():
            dho_message = DhOMessage.parse_raw(line)
            messages.append(dho_message)

    return messages
