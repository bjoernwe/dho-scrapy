from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.utils.paths import jsonl_path


def main():
    message_db = MessageDB.from_file(jsonl_path=jsonl_path)
    example_message_filtering(message_db=message_db)


def example_message_filtering(message_db: MessageDB):
    """
    Two examples for how to load and filter DhO messages through the MessageDB interface.
    """

    # EXAMPLE 1:
    # Load dharma diagnostics questions (i.e., all the initial posts that started a thread)
    diagnostic_questions = (
        message_db.filter_categories(categories={DhOCategory.DharmaDiagnostics})
        .filter_thread_responses(keep_op=False)
        .get_all_messages()
    )

    # Print first dharma diagnostics questions
    print(f"Found {len(diagnostic_questions)} questions from Dharma Diagnostics:\n")
    for question in diagnostic_questions[:3]:
        print(question.msg)
    print("...\n")

    # EXAMPLE 2
    # Load practice logs of a certain user
    author_id = "Linda ”Polly Ester” Ö"
    practice_logs = (
        message_db.filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_threads(authors={author_id})
        .filter_thread_responses(keep_op=True)
        .sorted_by_date()
        .get_all_messages()
    )

    # Print first practice logs
    print(f'Found {len(practice_logs)} practice logs from user "{author_id}":\n')
    for log in practice_logs[:3]:
        print(log.msg)
    print("...\n")


if __name__ == "__main__":
    main()
