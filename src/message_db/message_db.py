from collections import defaultdict
from pathlib import Path
from typing import List, Dict

from dho_scraper.items import DhOMessage


class MessageDB:

    def __init__(self, msgs: List[DhOMessage]):
        self._msgs = msgs

    @classmethod
    def from_file(cls, jsonl_path: Path) -> 'MessageDB':

        msgs = []

        with open(jsonl_path, 'r') as f:
            for line in f.readlines():
                msg = DhOMessage.parse_raw(line)
                msgs.append(msg)

        return cls(msgs=msgs)

    def __len__(self):
        return self._msgs.__len__()

    def get_all_messages(self) -> List[DhOMessage]:
        return self._msgs.copy()

    def get_all_message_bodies(self) -> List[str]:
        return [msg.msg for msg in self.get_all_messages()]

    def sorted_by_date(self) -> 'MessageDB':
        sorted_msgs = sorted(self.get_all_messages(), key=lambda m: m.date)
        return MessageDB(msgs=sorted_msgs)

    def group_by_author(self) -> Dict[str, 'MessageDB']:

        author_msgs: dict = defaultdict(list)

        for msg in self._msgs:
            author_msgs[msg.author].append(msg)

        return {author: MessageDB(messages) for author, messages in author_msgs.items()}

    def group_by_category(self) -> Dict[str, 'MessageDB']:

        category_msgs: dict = defaultdict(list)

        for msg in self._msgs:
            category_msgs[msg.category].append(msg)

        return {category: MessageDB(messages) for category, messages in category_msgs.items()}
