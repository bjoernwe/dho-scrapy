import os
from datetime import datetime
from pathlib import Path
from typing import List

import pytest
from _pytest.tmpdir import TempPathFactory
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from data_tools.dho_message import ForumMessage
from data_tools.message_db import MessageDB
from scraper.dho_scraper.categories import DhOCategory
from scraper.dho_scraper.spider import DhOSpider


@pytest.fixture
def dho_msg() -> ForumMessage:
    return ForumMessage(
        msg_id=15662490,
        category=DhOCategory.ContemporaryBuddhism,
        thread_id=15662491,
        title="10 things you disagree with Classical Buddhism",
        author="material-size",
        date=datetime(2019, 9, 14, 8, 13, 24),
        msg="Lists are handy things, and in this case they line up with brain wave function.<br /><br />I&#39;ll be surprised.",
        is_first_in_thread=False,
    )


@pytest.fixture(scope="session")
def session_tmp_path(tmp_path_factory: TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("dho-scraper")


@pytest.fixture(scope="session")
def test_dho_category() -> DhOCategory:
    return DhOCategory.ContemporaryBuddhism


@pytest.fixture(scope="session")
def scrapy_settings() -> Settings:
    old_cwd = os.getcwd()
    scraper_path = Path(__file__).parent.parent.joinpath("scraper")
    os.chdir(str(scraper_path))
    yield get_project_settings()
    os.chdir(old_cwd)


@pytest.fixture(scope="session")
def jsonl_path(
    session_tmp_path: Path, test_dho_category: DhOCategory, scrapy_settings: Settings
) -> Path:

    jsonl_out_path = session_tmp_path.joinpath("items.jsonl")

    scrapy_settings["FEEDS"][str(jsonl_out_path)] = {"format": "jsonlines"}
    scrapy_settings["PIPELINE_MIN_MESSAGE_WORDS"] = 1

    process = CrawlerProcess(settings=scrapy_settings)
    process.crawl(DhOSpider, categories=[test_dho_category])
    process.start()

    return jsonl_out_path


@pytest.fixture(scope="session")
def message_db(jsonl_path: Path) -> MessageDB:
    return MessageDB.from_file(jsonl_path=jsonl_path)


@pytest.fixture(scope="session")
def crawled_messages(jsonl_path: Path) -> List[ForumMessage]:
    return _messages_from_file(jsonl_path)


def _messages_from_file(jsonl_path: Path) -> List[ForumMessage]:

    messages = []

    with open(str(jsonl_path), "r") as file:
        for line in file.readlines():
            dho_message = ForumMessage.parse_raw(line)
            messages.append(dho_message)

    return messages
