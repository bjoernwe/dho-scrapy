import pandas as pd

from data_tools.default_paths import default_jsonl_path
from data_tools.dho_categories import DhOCategory
from data_tools.message_db import MessageDB


def main():

    # Get text
    msg_db = MessageDB.from_file(jsonl_path=default_jsonl_path)
    snippets = (
        msg_db.filter_categories(categories={DhOCategory.DharmaDiagnostics})
        .filter_message_length(min_num_words=3)
        .get_snippet_texts(sentences_per_snippet=3)
    )

    # Create DataFrame
    df = pd.DataFrame(snippets, columns=["Text"])
    df = df.sample(frac=1).reset_index(drop=True)  # shuffle
    print(df)

    # Write CSV
    csv_file_name = "text.csv"
    df.to_csv(csv_file_name, index=False)
    print(f"Wrote text data to {csv_file_name}")


if __name__ == "__main__":
    main()
