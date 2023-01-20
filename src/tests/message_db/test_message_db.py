from typing import List, Any, Callable

import pytest

from dho_scraper.categories import DhOCategory
from dho_scraper.items import DhOMessage
from message_db.message_db import MessageDB


@pytest.fixture
def message_db(jsonl_path) -> MessageDB:
    return MessageDB.from_file(jsonl_path=jsonl_path)


@pytest.fixture
def msgs_in_threads(dho_msg: DhOMessage) -> List[DhOMessage]:

    author_1 = 'AUTHOR 1'
    author_2 = 'AUTHOR 2'
    thread_1 = 111
    thread_2 = 222

    msg1 = dho_msg.copy()
    msg1.author = author_1
    msg1.thread_id = thread_1
    msg1.is_first_in_thread = True

    msg2 = dho_msg.copy()
    msg2.author = author_2
    msg2.thread_id = thread_2
    msg2.is_first_in_thread = True

    msg3 = dho_msg.copy()
    msg3.author = author_1
    msg3.thread_id = thread_2

    return [msg1, msg2, msg3]


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


def test_category_groups_are_filtered_for_length(dho_msg: DhOMessage):

    # GIVEN a list of messages in two categories
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].category = 'CATEGORY_1'
    msgs[1].category = msgs[2].category = 'CATEGORY_2'

    # WHEN messages are grouped by author
    category_msgs = MessageDB(msgs=msgs).group_by_category(min_num_messages=2)

    # THEN all messages are in the groups
    assert 'CATEGORY_1' not in category_msgs
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


def test_thread_grouping_contains_all_messages(msgs_in_threads: List[DhOMessage]):

    # GIVEN a list of messages in two threads
    db = MessageDB(msgs=msgs_in_threads)

    # WHEN messages are grouped by author
    thread = db.group_by_thread()

    # THEN all messages are in the groups
    assert len(thread[111]) == 1
    assert len(thread[222]) == 2


def test_thread_groups_are_filtered_by_size(msgs_in_threads: List[DhOMessage]):

    # GIVEN a list of messages in two threads
    db = MessageDB(msgs=msgs_in_threads)

    # WHEN messages are grouped by author
    thread_messages = db.group_by_thread(min_num_messages=2)

    # THEN all messages are in the groups
    assert 111 not in thread_messages
    assert len(thread_messages[222]) == 2
    assert len(thread_messages) == 1


def test_thread_responses_are_filtered_out(message_db: MessageDB):

    # GIVEN a MessageDB
    # WHEN threads are filtered (remove all responses to initial post)
    db = message_db.filter_thread_responses(keep_op=False)

    # THEN each thread has exactly one message
    assert len(db) >= 1
    for thread_id, msgs in db.group_by_thread().items():
        assert len(msgs) == 1
        assert msgs[0].is_first_in_thread


def test_non_op_thread_responses_are_filtered_out(message_db: MessageDB):

    # GIVEN a MessageDB
    # WHEN threads are filtered for OP-responses ("Original Poster")
    db = message_db.filter_thread_responses(keep_op=True)

    # THEN each thread has exactly one message
    for thread_messages in db.group_by_thread().values():
        authors_in_thread = {msg.author for msg in thread_messages.get_all_messages()}
        assert len(authors_in_thread) == 1


def test_authors_are_filtered(dho_msg: DhOMessage):

    # GIVEN a list of messages from two authors
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].author = 'AUTHOR_1'
    msgs[1].author = msgs[2].author = 'AUTHOR_2'

    # WHEN messages are filtered for one author
    author_msgs = MessageDB(msgs=msgs).filter_authors(authors={'AUTHOR_1'}).group_by_author()

    # THEN the only this author remains
    assert len(author_msgs) == 1
    assert 'AUTHOR_1' in author_msgs


def test_authors_are_filtered_with_min_message_number(dho_msg: DhOMessage):

    # GIVEN a list of messages from two authors
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].author = 'AUTHOR_1'
    msgs[1].author = msgs[2].author = 'AUTHOR_2'

    # WHEN messages are filtered for one author
    authors = {'AUTHOR_1', 'AUTHOR_2'}
    filtered_msgs = MessageDB(msgs=msgs).filter_authors(authors=authors, min_num_messages=2).get_all_messages()

    # THEN all messages are in the groups
    assert len(filtered_msgs) == 2
    assert filtered_msgs[0].author == filtered_msgs[0].author == 'AUTHOR_2'


def test_filtering_no_authors_keeps_all_authors(dho_msg: DhOMessage):

    # GIVEN a list of messages from two authors
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].author = 'AUTHOR_1'
    msgs[1].author = msgs[2].author = 'AUTHOR_2'

    # WHEN messages are filtered for author, no author specified
    filtered_db = MessageDB(msgs=msgs).filter_authors()

    # THEN all messages are kept
    assert len(filtered_db) == 3


@pytest.mark.parametrize(argnames='key', argvalues=[lambda m: m.author,
                                                    lambda m: m.thread_id,
                                                    lambda m: m.category])
def test_groups_are_sorted_for_size(message_db: MessageDB, key: Callable[[DhOMessage], Any]):

    # GIVEN a DB of messages
    # WHEN they are grouped
    group_dict = message_db._group_messages(key=key)

    # THEN the resulting groups are sorted for number of messages
    group_lengths = list(map(lambda db: len(db), group_dict.values()))
    assert group_lengths == sorted(group_lengths, reverse=True)


@pytest.mark.parametrize(argnames='key', argvalues=[lambda m: m.author,
                                                    lambda m: m.thread_id,
                                                    lambda m: m.category])
def test_groups_are_filtered_for_size(message_db: MessageDB, key: Callable[[DhOMessage], Any]):

    # GIVEN a DB of messages
    # WHEN they are grouped with size filter
    group_dict = message_db._group_messages(key=key, min_group_size=5)

    # THEN the resulting groups are sorted for number of messages
    for group_msgs in group_dict.values():
        assert len(group_msgs) >= 5


def test_categories_are_filtered(dho_msg: DhOMessage):

    # GIVEN a list of messages in two categories
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].category = DhOCategory.DharmaDiagnostics
    msgs[1].category = msgs[2].category = DhOCategory.PracticeLogs

    # WHEN messages are filtered for author, no author specified
    filtered_db = MessageDB(msgs=msgs).filter_categories(categories={DhOCategory.PracticeLogs})

    # THEN all messages are kept
    assert len(filtered_db) == 2


def test_filtering_no_category_keeps_all_categories(dho_msg: DhOMessage):

    # GIVEN a list of messages in two categories
    msgs = [dho_msg.copy() for _ in range(3)]
    msgs[0].category = 'CATEGORY_1'
    msgs[1].category = msgs[2].category = 'CATEGORY_2'

    # WHEN messages are filtered for author, no author specified
    filtered_db = MessageDB(msgs=msgs).filter_categories()

    # THEN all messages are kept
    assert len(filtered_db) == 3


def test_threads_are_filtered_with_min_message_number(msgs_in_threads: List[DhOMessage]):

    # GIVEN a list of messages in two threads
    db = MessageDB(msgs=msgs_in_threads)

    # WHEN messages are filtered for one author
    filtered_msgs = db.filter_threads(min_num_messages=2).get_all_messages()

    # THEN all messages are in the groups
    assert len(filtered_msgs) == 2
    assert filtered_msgs[0].thread_id == filtered_msgs[0].thread_id == 222


def tests_threads_are_filtered_for_thread_author(msgs_in_threads: List[DhOMessage]):

    # GIVEN a list of messages in two threads
    db = MessageDB(msgs=msgs_in_threads)

    # WHEN the threads are filtered for one author
    filtered_msgs = db.filter_threads(authors={'AUTHOR 2'}).get_all_messages()

    # THEN left are the two message in the thread with corresponding author
    assert len(filtered_msgs) == 2
    assert filtered_msgs[0].thread_id == filtered_msgs[1].thread_id == 222
    assert filtered_msgs[0].author == 'AUTHOR 2'
    assert filtered_msgs[1].author == 'AUTHOR 1'
