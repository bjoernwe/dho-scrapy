from pathlib import Path
from typing import List

from dho_scraper.items import DhOMessage


def read_dho_messages(jsonl_path: Path) -> List[DhOMessage]:

    messages = []

    with open(jsonl_path, 'r') as f:
        for line in f.readlines():
            msg = DhOMessage.parse_raw(line)
            messages.append(msg)

    return messages


def read_strings(file: str) -> List[str]:

    strings = []

    with open(file, 'r') as f:
        for line in f.readlines():
            strings.append(line)

    return strings


def save_strings(strings: List[str], output_file: str):
    with open(output_file, 'w') as f:
        f.writelines('\n'.join(strings))
