from datetime import datetime

import pytest

from data_tools.dho_message import DhOMessage


def test_dho_message_accepts_datetime(dho_msg: DhOMessage):

    # GIVEN messsage parameters with date as datetime
    date = datetime(2020, 11, 21, 4, 14, 6)
    msg_dict = dho_msg.dict()
    msg_dict["date"] = date

    # WHEN a DhO message is created
    msg = DhOMessage.parse_obj(msg_dict)

    # THEN the date was not changed
    assert msg.date == date


def test_dho_message_accepts_date_string_in_dho_format(dho_msg: DhOMessage):

    # GIVEN messsage parameters with date as string
    date = "Sat, 21 Nov 2020 04:14:06 GMT"
    msg_dict = dho_msg.dict()
    msg_dict["date"] = date

    # WHEN a message is created with this input format
    msg = DhOMessage.parse_obj(msg_dict)

    # THEN the resulting message contains the correct date
    assert msg.date == datetime(2020, 11, 21, 4, 14, 6)


def test_message_is_split_into_sentences(dho_msg: DhOMessage):

    # GIVEN a message that contains several sentences
    dho_msg.msg = "This is sentence 1. This is sentence two. This is another one."

    # WHEN the individual sentences are queried
    sentences = dho_msg.sentences

    # THEN they are split correctly
    snts = [s.text for s in sentences]
    assert snts == [
        "This is sentence 1.",
        "This is sentence two.",
        "This is another one.",
    ]


def test_subsequent_sentences_are_concatenated_in_sliding_window(dho_msg: DhOMessage):

    # GIVEN a message that contains several sentences
    dho_msg.msg = "This is sentence 1. This is sentence two. This is another one."

    # WHEN a window of sentences is extracted
    sentences = dho_msg.get_snippets(sentences_per_snippet=2)

    # THE result is as expected
    snts = [s.text for s in sentences]
    assert snts == [
        "This is sentence 1. This is sentence two.",
        "This is sentence two. This is another one.",
    ]


@pytest.mark.parametrize(argnames="window_size", argvalues=[3, 4])
def test_sentence_windows_work_with_extreme_values(
    dho_msg: DhOMessage,
    window_size: int,
):

    # GIVEN a message that contains several sentences
    dho_msg.msg = "This is sentence 1. This is sentence two. This is another one."

    # WHEN a window of unreasonable size is requested
    sentences = dho_msg.get_snippets(sentences_per_snippet=window_size)

    # THEN the result is the original sentence
    assert len(sentences) == 1
    assert sentences[0].text == dho_msg.msg


def test_sentences_can_be_calculated_for_empty_message(dho_msg: DhOMessage):

    # GIVEN a message with empty body
    dho_msg.msg = ""

    # WHEN sentence snippets are calculated
    snippets = dho_msg.get_snippets(sentences_per_snippet=2)

    # THEN it is an empty list
    assert snippets == []
