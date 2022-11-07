from pathlib import Path
from typing import List

import pytest

from _pytest.tmpdir import TempPathFactory
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.items import DhOMessage
from scraper.spiders.DhOSpider import DhOSpider, DhOCategory


@pytest.fixture(scope='session')
def items_jsonl_path(tmp_path_factory: TempPathFactory) -> Path:

    tmp_path = tmp_path_factory.mktemp('dho-scraper')
    tmp_items_path = tmp_path.joinpath('items.jsonl')
    DhOSpider.set_output_feed(jsonlines_path=str(tmp_items_path))

    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(DhOSpider, categories=[DhOCategory.ContemporaryBuddhism])
    process.start()

    return tmp_items_path


@pytest.fixture()
def dho_messages(items_jsonl_path: Path) -> List[DhOMessage]:

    messages = []

    with open(str(items_jsonl_path), 'r') as file:
        for line in file.readlines():
            dho_message = DhOMessage.parse_raw(line)
            messages.append(dho_message)

    return messages


def test_spider_finds_expected_number_of_messages(dho_messages: List[DhOMessage]):
    # GIVEN a spider for DhO
    # WHEN the messages are crawled
    # THEN there's the expected number of them
    assert len(dho_messages) >= 678


def test_spider_finds_known_message(dho_messages: List[DhOMessage]):

    # GIVEN a known message from DhO
    known_message = DhOMessage(
        title='RE: Hippie Dippy Bulls**t',
        msg='I think people often have a hard time holding more than one thought in their mind. That makes it hard to be nuanced.\xa0'
    )

    # WHEN all messages are crawled
    # THEN the result contains a known message
    assert known_message in dho_messages
