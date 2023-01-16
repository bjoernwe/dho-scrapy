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


def test_author_grouping_contains_all_messages(dho_msg: DhOMessage):

    # GIVEN a list of messages from two authors
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].author = 'AUTHOR_1'
    msgs[1].author = msgs[2].author = 'AUTHOR_2'

    # WHEN messages are grouped by author
    author_msgs = MessageDB(msgs=msgs).group_by_author()

    # THEN all messages are in the groups
    assert len(author_msgs['AUTHOR_1']) == 1
    assert len(author_msgs['AUTHOR_2']) == 2


def test_author_grouping_is_filtered_for_min_num_messages(dho_msg: DhOMessage):

    # GIVEN a list of messages from two authors
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].author = 'AUTHOR_1'
    msgs[1].author = msgs[2].author = 'AUTHOR_2'

    # WHEN messages are grouped by author
    author_msgs = MessageDB(msgs=msgs).group_by_author(min_num_messages=2)

    # THEN all messages are in the groups
    assert 'AUTHOR_1' not in author_msgs
    assert len(author_msgs['AUTHOR_2']) == 2


def test_messages_are_sorted_by_date(message_db: MessageDB):

    # GIVEN a message DB with messages not sorted by date
    msgs = message_db.get_all_messages()
    assert False in [msgs[i].date <= msgs[i+1].date for i in range(len(msgs)-1)]

    # WHEN the DB is sorted
    sorted_msgs = message_db.sorted_by_date().get_all_messages()

    # THEN all resulting messages are sorted
    assert False not in [sorted_msgs[i].date <= sorted_msgs[i+1].date for i in range(len(msgs)-1)]


def test_category_grouping_contains_all_messages(dho_msg: DhOMessage):

    # GIVEN a list of messages in two categories
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].category = 'CATEGORY_1'
    msgs[1].category = msgs[2].category = 'CATEGORY_2'

    # WHEN messages are grouped by author
    category_msgs = MessageDB(msgs=msgs).group_by_category()

    # THEN all messages are in the groups
    assert len(category_msgs['CATEGORY_1']) == 1
    assert len(category_msgs['CATEGORY_2']) == 2


def test_messages_are_filtered_for_length(dho_msg: DhOMessage):

    # GIVEN messages of different lengths
    msgs = [dho_msg.copy() for _ in range(2)]
    msgs[0].msg = 'two words'
    msgs[1].msg = 'two plus words'

    # WHEN they are filtered for their length
    filtered_msgs = MessageDB(msgs=msgs) \
        .filter_message_length(min_num_words=3) \
        .get_all_messages()

    # THEN the short message was filtered out
    assert len(filtered_msgs) == 1
    assert filtered_msgs[0].msg == 'two plus words'


def test_thread_grouping_contains_all_messages(dho_msg: DhOMessage):

    # GIVEN a list of messages in two threads
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].thread_id = 111
    msgs[1].thread_id = msgs[2].thread_id = 222

    # WHEN messages are grouped by author
    thread = MessageDB(msgs=msgs).group_by_thread()

    # THEN all messages are in the groups
    assert len(thread[111]) == 1
    assert len(thread[222]) == 2


def test_thread_responses_are_filtered_out(message_db: MessageDB):

    # GIVEN a MessageDB
    # WHEN threads are filtered (remove all responses to initial post)
    db = message_db.filter_thread_responses()

    # THEN each thread has exactly one message
    for thread_id, msgs in db.group_by_thread().items():
        assert len(msgs) == 1
