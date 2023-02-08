from experiments.utils.messages import message_db
from scraper.dho_scraper.categories import DhOCategory


def example_message_filtering():
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
    example_message_filtering()
