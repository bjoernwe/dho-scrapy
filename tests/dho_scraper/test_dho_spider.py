from pathlib import Path
from typing import List

from data_models.dho_message import DhOMessage
from scraper.dho_scraper.spider import DhOCategory
from scraper.dho_scraper.spider import DhOSpider


def test_spider_finds_expected_number_of_messages(crawled_messages: List[DhOMessage]):
    # GIVEN a spider for DhO
    # WHEN the messages are crawled
    # THEN there's the expected number of them
    assert len(crawled_messages) >= 31


def _find_msg_by_id(msg_id: int, msgs: List[DhOMessage]) -> DhOMessage:
    return next(filter(lambda m: m.msg_id == msg_id, msgs))


def test_spider_finds_known_message(
    crawled_messages: List[DhOMessage], dho_msg: DhOMessage
):
    # GIVEN a known message
    # WHEN all messages are crawled by the spider
    # THEN they contain the known message
    msg = _find_msg_by_id(msg_id=dho_msg.msg_id, msgs=crawled_messages)
    assert msg.title == dho_msg.title
    assert msg.author == dho_msg.author


def test_spider_removes_html(crawled_messages: List[DhOMessage], dho_msg: DhOMessage):

    # GIVEN a DhO spider and a known message with HTML tags
    assert "<" in dho_msg.msg

    # WHEN the known message has been crawled
    msg = _find_msg_by_id(msg_id=dho_msg.msg_id, msgs=crawled_messages)

    # THEN it does not contain HTML tags
    assert "<" not in msg.msg


def test_spider_parses_message_ids(crawled_messages: List[DhOMessage]):

    # GIVEN a list of messages crawled by the spider
    # WHEN the message IDs are considered
    msg_ids = {msg.msg_id for msg in crawled_messages}

    # THEN all messages have a unique ID
    assert len(msg_ids) == len(crawled_messages)


def test_crawled_messages_contain_category(
    crawled_messages: List[DhOMessage], test_dho_category: DhOCategory
):

    # GIVEN spider and a certain category
    # WHEN the message are crawled
    # THEN they all contain the specified category
    for msg in crawled_messages:
        assert msg.category == test_dho_category


def test_feed_output_contains_uri_scheme():

    # GIVEN a DhOSpider
    spider = DhOSpider()

    # WHEN an output file is set
    path = Path("foo")
    spider.set_output_feed(jsonlines_path=path)

    # THEN scrapy is configured with a file:// scheme
    # (otherwise, on Windows, "C:" would be interpreted as scheme)
    feed_files: List[str] = list(spider.custom_settings["FEEDS"].keys())
    assert len(feed_files) == 1
    assert feed_files[0].startswith("file://")


def test_crawled_messages_are_redacted(crawled_messages: List[DhOMessage]):

    # GIVEN a list of messages crawled by the spider
    # WHEN all authors are collected
    authors = {msg.author for msg in crawled_messages}

    # THEN it contains redacted versions of known author names
    assert "materialistic-gift" in authors
