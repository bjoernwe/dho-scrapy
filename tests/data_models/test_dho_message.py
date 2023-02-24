from datetime import datetime

from data_models.dho_message import DhOMessage


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
    snts = [s.sentence for s in sentences]
    assert snts == [
        "This is sentence 1.",
        "This is sentence two.",
        "This is another one.",
    ]
