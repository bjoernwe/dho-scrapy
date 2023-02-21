from data_models.message_db import MessageDB
from examples.example_message_filtering import example_message_filtering


def test_example_runs_without_error(message_db: MessageDB):
    example_message_filtering(message_db=message_db)
