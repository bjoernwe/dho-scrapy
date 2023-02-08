from datetime import datetime

from scraper.dho_scraper.items import DhOMessage


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
