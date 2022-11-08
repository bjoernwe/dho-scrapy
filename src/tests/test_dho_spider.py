from datetime import timezone, datetime
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


def _find_msg_by_date(dt: datetime, msgs: List[DhOMessage]) -> DhOMessage:
    return next(filter(lambda m: m.date == dt, msgs))


def test_spider_finds_known_message(dho_messages: List[DhOMessage]):

    # GIVEN a known message from DhO
    known_msg = DhOMessage(
        title='RE: Hippie Dippy Bulls**t',
        author='Milo',
        date=datetime(2020, 11, 21, 4, 14, 6),
        msg='<img src="https://i.redd.it/disdm1grojj21.jpg" />'  # Warning: Pipeline may change HTML formatting!
    )

    # WHEN all messages are crawled
    msg = _find_msg_by_date(dt=known_msg.date, msgs=dho_messages)

    # THEN the result contains the known message
    assert msg.title == known_msg.title
    assert msg.author == known_msg.author


def test_spider_removes_block_quotes(dho_messages: List[DhOMessage]):

    # GIVEN a DhO message that is known to contain a blockquote
    known_msg = DhOMessage(
        title='RE: Letter and Invitation: Living Buddhas in Pemako Sangha',
        author='George S',
        date=datetime(2022, 6, 30, 17, 41, 42),
        msg='<div class="quote"><div class="quote-content">Kim Katami<br />I haven&#39;t written posts like this in a long time but for some reason I did so today.<br /></div></div><br />If I had to guess:<br /><br />73 x 30 = 2,190<br /><br />Buddha inflation <img alt="emoticon" src="https://www.dharmaoverground.org/o/classic-theme/images/emoticons/tongue.gif" >',
    )

    # WHEN all messages are crawled
    msg = _find_msg_by_date(dt=known_msg.date, msgs=dho_messages)

    # THEN the known message does not contain the blockquote
    assert 'Katami' not in msg.msg
