from data_models.categories import DhOCategory
from data_models.message_db import MessageDB
from experiments.utils.paths import jsonl_path


def main():
    print_practice_log_counts()


def print_practice_log_counts():

    author_logs = (
        MessageDB.from_file(jsonl_path=jsonl_path)
        .filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_thread_responses(keep_op=True)
        .group_by_author()
    )

    for author, msgs in author_logs.items():
        print(f"{len(msgs)}: {author}")


if __name__ == "__main__":
    main()
