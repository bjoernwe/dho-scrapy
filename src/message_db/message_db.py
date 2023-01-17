from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Callable, Any, Hashable, Set, Optional

from dho_scraper.items import DhOMessage


class MessageDB:
    """
    MessageDB serves a convenient interface to a list of DhO messages - as crawled by dho-scrapy, for instance. The
    interface provides methods for filtering, grouping, and sorting the messages according to criteria like author,
    thread, etc.
    """

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

    def _group_messages(self, key: Callable[[DhOMessage], Any]) -> Dict[Hashable, List[DhOMessage]]:

        grouped_msgs = defaultdict(list)

        for msg in self._msgs:
            group = key(msg)
            grouped_msgs[group].append(msg)

        return grouped_msgs

    def group_by_author(self, min_num_messages: int = 1) -> Dict[str, 'MessageDB']:
        author_msgs = self._group_messages(key=lambda m: m.author)
        return {author: MessageDB(messages)
                for author, messages in author_msgs.items()
                if len(messages) >= min_num_messages}

    def group_by_category(self) -> Dict[str, 'MessageDB']:
        category_msgs = self._group_messages(key=lambda m: m.category)
        return {category: MessageDB(messages) for category, messages in category_msgs.items()}

    def group_by_thread(self) -> Dict[int, 'MessageDB']:
        thread_msgs = self._group_messages(key=lambda m: m.thread_id)
        return {thread_id: MessageDB(messages) for thread_id, messages in thread_msgs.items()}

    def filter_message_length(self, min_num_words: int = 1) -> 'MessageDB':
        msgs = [msg for msg in self._msgs if len(msg.msg.split()) >= min_num_words]
        return MessageDB(msgs=msgs)

    def filter_thread_responses(self, keep_op: bool) -> 'MessageDB':
        filtered_msgs = [msg for msg in self.get_all_messages() if msg.is_first_in_thread]
        if keep_op:
            thread_author = {msg.thread_id: msg.author for msg in filtered_msgs}
            filtered_msgs = [msg for msg
                             in self.get_all_messages()
                             if msg.is_first_in_thread
                             or msg.author == thread_author[msg.thread_id]]
        return MessageDB(msgs=filtered_msgs)

    def filter_authors(self, authors: Optional[Set[str]] = None, min_num_messages: int = 1) -> 'MessageDB':
        author_msgs = self.group_by_author(min_num_messages=min_num_messages)
        filtered_msgs = [msg for author, msgs in author_msgs.items()
                         for msg in msgs.get_all_messages()
                         if authors is None or author in authors]
        return MessageDB(msgs=filtered_msgs)
