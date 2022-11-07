from pathlib import Path

import pytest
from scrapy.http import XmlResponse

from scraper.spiders import DhOSpider


@pytest.fixture(scope='session')
def rss_data() -> str:
    rss_file = Path(__file__).parent.joinpath('data/rss.xml')
    with open(rss_file, 'r') as file:
        data = file.read()
    return data


@pytest.fixture
def rss_response(rss_data: str) -> XmlResponse:
    return XmlResponse(
        url='https://www.dharmaoverground.org/c/message_boards/rss?plid=10262&groupId=10128&threadId=21844394&max=1000&type=rss&version=2.0',
        encoding='utf-8',
        body=rss_data
    )


def test_all_messages_are_parsed_from_rss(rss_response: XmlResponse):

    # GIVEN the response object for an RSS
    # WHEN the RSS response is parsed
    messages = list(DhOSpider._get_messages_from_rss(response=rss_response))

    # THEN all messages are found
    assert len(messages) == 23
