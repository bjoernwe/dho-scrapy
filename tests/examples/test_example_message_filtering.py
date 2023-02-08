from examples.example_message_filtering import example_message_filtering
from scraper.message_db.message_db import MessageDB


def test_example_runs_without_error(message_db: MessageDB):
    example_message_filtering(message_db=message_db)
