from datetime import datetime
from pathlib import Path
from typing import List

import pytest

from _pytest.tmpdir import TempPathFactory
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dho_scraper.items import DhOMessage
from dho_scraper.spider import DhOSpider, DhOCategory


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
def crawled_messages(items_jsonl_path: Path) -> List[DhOMessage]:

    messages = []

    with open(str(items_jsonl_path), 'r') as file:
        for line in file.readlines():
            dho_message = DhOMessage.parse_raw(line)
            messages.append(dho_message)

    return messages


def test_spider_finds_expected_number_of_messages(crawled_messages: List[DhOMessage]):
    # GIVEN a spider for DhO
    # WHEN the messages are crawled
    # THEN there's the expected number of them
    assert len(crawled_messages) >= 31


def _find_msg_by_id(msg_id: int, msgs: List[DhOMessage]) -> DhOMessage:
    return next(filter(lambda m: m.msg_id == msg_id, msgs))


def test_spider_finds_known_message(crawled_messages: List[DhOMessage], dho_msg: DhOMessage):
    # GIVEN a known message
    # WHEN all messages are crawled by the spider
    # THEN they contain the known message
    msg = _find_msg_by_id(msg_id=dho_msg.msg_id, msgs=crawled_messages)
    assert msg.title == dho_msg.title
    assert msg.author == dho_msg.author


def test_spider_removes_html(crawled_messages: List[DhOMessage], dho_msg: DhOMessage):

    # GIVEN a DhO spider and a known message with HTML tags
    assert '<' in dho_msg.msg

    # WHEN the known message has been crawled
    msg = _find_msg_by_id(msg_id=dho_msg.msg_id, msgs=crawled_messages)

    # THEN it does not contain HTML tags
    assert '<' not in msg.msg


def test_spider_parses_message_ids(crawled_messages: List[DhOMessage]):

    # GIVEN a list of messages crawled by the spider
    # WHEN the message IDs are considered
    msg_ids = {msg.msg_id for msg in crawled_messages}

    # THEN all messages have a unique ID
    assert len(msg_ids) == len(crawled_messages)
