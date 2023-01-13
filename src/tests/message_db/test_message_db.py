from typing import List

import pytest

from dho_scraper.items import DhOMessage
from message_db.message_db import MessageDB


@pytest.fixture
def message_db(jsonl_path) -> MessageDB:
    return MessageDB.from_file(jsonl_path=jsonl_path)


def test_all_messages_are_returned(jsonl_path, crawled_messages: List[DhOMessage]):

    # GIVEN a list of messages
    assert len(crawled_messages) >= 1

    # WHEN a message DB is created for those messages
    db = MessageDB.from_file(jsonl_path=jsonl_path)

    # THEN all messages can be queried from the DB
    assert len(db.get_all_messages()) == len(crawled_messages)


def test_messages_are_grouped_by_author(message_db: MessageDB):

    # GIVEN a message DB
    # WHEN the messages are grouped by author
    author_msgs = message_db.group_by_author()

    # THEN there are messages of at least one of the known authors
    assert len(author_msgs['J W']) >= 7
