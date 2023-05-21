from data_tools.default_paths import default_jsonl_path
from data_tools.message_db import MessageDB
from scraper.spiders.dho.categories import DhOCategory


def main():
    print_practice_log_counts()


def print_practice_log_counts():

    author_logs = (
        MessageDB.from_file(jsonl_path=default_jsonl_path)
        .filter_categories(categories={DhOCategory.PracticeLogs})
        .filter_thread_responses(keep_op=True)
        .group_by_author()
    )

    for author, msgs in author_logs.items():
        print(f"{len(msgs)}: {author}")


if __name__ == "__main__":
    main()
