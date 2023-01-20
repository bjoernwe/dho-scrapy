from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Callable, Any, Hashable, Set, Optional

from dho_scraper.categories import DhOCategory
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

    def __getitem__(self, item):
        return self._msgs[item]

    def get_all_messages(self) -> List[DhOMessage]:
        return self._msgs.copy()

    def get_all_message_bodies(self) -> List[str]:
        return [msg.msg for msg in self.get_all_messages()]

    def sorted_by_date(self) -> 'MessageDB':
        sorted_msgs = sorted(self.get_all_messages(), key=lambda m: m.date)
        return MessageDB(msgs=sorted_msgs)

    def _group_messages(self,
                        key: Callable[[DhOMessage], Any],
                        keep_keys: Optional[Set[Hashable]] = None,
                        min_group_size: int = 1) -> Dict[Hashable, 'MessageDB']:

        grouped_msgs = defaultdict(list)

        for msg in self._msgs:
            group = key(msg)
            grouped_msgs[group].append(msg)

        filtered_msgs = {k: v
                         for k, v in grouped_msgs.items()
                         if len(v) >= min_group_size                 # filter length
                         and (keep_keys is None or k in keep_keys)}  # filter keys (if specified)

        sorted_dict = dict(sorted(filtered_msgs.items(), key=lambda kv: len(kv[1]), reverse=True))
        return {k: MessageDB(msgs=v) for k, v in sorted_dict.items()}

    def group_by_author(self, keep_authors: Optional[Set[str]] = None, min_num_messages: int = 1) -> Dict[str, 'MessageDB']:
        return self._group_messages(key=lambda m: m.author,
                                    keep_keys=keep_authors,
                                    min_group_size=min_num_messages)

    def group_by_category(self, keep_categories: Optional[Set] = None, min_num_messages: int = 1) -> Dict[str, 'MessageDB']:
        return self._group_messages(key=lambda m: m.category,
                                    keep_keys=keep_categories,
                                    min_group_size=min_num_messages)

    def group_by_thread(self, min_num_messages: int = 1) -> Dict[int, 'MessageDB']:
        thread_msgs = self._group_messages(key=lambda m: m.thread_id, min_group_size=min_num_messages)
        for tid, msgs in thread_msgs.items():
            assert thread_msgs[tid][0].is_first_in_thread, "Expecting thread groups to be sorted in a way that the initial post is first!"
        return thread_msgs

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
                             or msg.author == thread_author.get(msg.thread_id)]
        return MessageDB(msgs=filtered_msgs)

    def filter_authors(self, authors: Optional[Set[str]] = None, min_num_messages: int = 1) -> 'MessageDB':
        author_msgs = self.group_by_author(keep_authors=authors, min_num_messages=min_num_messages)
        filtered_msgs = [msg for author, msgs in author_msgs.items()
                         for msg in msgs.get_all_messages()]
        return MessageDB(msgs=filtered_msgs)

    def filter_categories(self, categories: Optional[Set[DhOCategory]] = None, min_num_message: int = 1) -> 'MessageDB':
        category_msgs = self.group_by_category(keep_categories=categories, min_num_messages=min_num_message)
        filtered_msgs = [msg for category, msgs in category_msgs.items()
                         for msg in msgs.get_all_messages()]
        return MessageDB(msgs=filtered_msgs)

    def filter_threads(self, authors: Optional[Set[str]] = None, min_num_messages: int = 1) -> 'MessageDB':
        thread_groups = self.group_by_thread(min_num_messages=min_num_messages)
        filtered_msgs = [msg for thread_id, thread_msgs in thread_groups.items()
                         for msg in thread_msgs.get_all_messages()
                         if authors is None or thread_msgs[0].author in authors]
        return MessageDB(msgs=filtered_msgs)
