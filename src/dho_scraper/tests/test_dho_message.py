from datetime import datetime

from dho_scraper.items import DhOMessage


def test_dho_message_accepts_datetime():

    # GIVEN a datetime object
    dt = datetime(2020, 11, 21, 4, 14, 6)

    # WHEN a DhO message is created
    msg = DhOMessage(
        title='title',
        author='author',
        date=dt,
        msg='msg',
        is_first_in_thread=True,
    )

    # THEN the date was not changed
    assert msg.date == dt


def test_dho_message_accepts_date_string_in_dho_format():

    # GIVEN a date string from DhO
    date_str = 'Sat, 21 Nov 2020 04:14:06 GMT'

    # WHEN a message is created with this input format
    msg = DhOMessage(
        title='title',
        author='author',
        date=date_str,
        msg='msg',
        is_first_in_thread=True,
    )

    # THEN the resulting message contains the correct date
    assert msg.date == datetime(2020, 11, 21, 4, 14, 6)
