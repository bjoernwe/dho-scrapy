# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from bs4 import BeautifulSoup
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from data_models.dho_message import DhOMessage


class RemoveDuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item: DhOMessage, _):

        msg_id = item.msg_id

        if msg_id in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")

        self.ids_seen.add(msg_id)
        return item


class RemoveNonOpRepliesPipeline:

    thread_owners = {}

    @classmethod
    def process_item(cls, item: DhOMessage, _):

        if item.is_first_in_thread:
            cls.thread_owners[item.thread_id] = item.author  # remember author

        thread_op = cls.thread_owners[item.thread_id]
        post_is_by_op = item.author == thread_op

        if item.is_first_in_thread or post_is_by_op:
            return item

        raise DropItem


class RemoveAllRepliesPipeline:
    @classmethod
    def process_item(cls, item: DhOMessage, _):
        if item.is_first_in_thread:
            return item
        raise DropItem


class RemoveDhOBlockquotesPipeline:
    def process_item(self, item, _):
        adapter = ItemAdapter(item)
        adapter["msg"] = self._remove_blockquotes(adapter["msg"])
        return item

    @staticmethod
    def _remove_blockquotes(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.findAll("div", class_="quote"):
            tag.decompose()
        return str(soup)


class HtmlToTextPipeline:
    def process_item(self, item, _):
        adapter = ItemAdapter(item)
        adapter["msg"] = self._html_to_text(adapter["msg"])
        return item

    @staticmethod
    def _html_to_text(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator=" ")


class ReplaceNonStandardWhitespacesPipeline:
    def process_item(self, item, _):
        adapter = ItemAdapter(item)
        adapter["msg"] = self._normalize_whitespaces(adapter["msg"])
        return item

    @staticmethod
    def _normalize_whitespaces(s: str) -> str:

        characters = [
            "\u00a0",  # non-breaking space
            "\u200b",  # zero-width space
        ]

        for c in characters:
            s = s.replace(c, " ")

        return s


class RemoveDuplicateSpacesPipeline:
    def process_item(self, item, _):
        adapter = ItemAdapter(item)
        adapter["msg"] = self._remove_duplicate_spaces(adapter["msg"])
        return item

    @staticmethod
    def _remove_duplicate_spaces(s: str):
        return " ".join(s.split())


class RemoveShortMessagePipeline:
    @classmethod
    def from_crawler(cls, crawler):
        min_message_words = crawler.settings.get("PIPELINE_MIN_MESSAGE_WORDS")
        return cls(min_message_words=min_message_words)

    def __init__(self, min_message_words: int = 1):
        self._min_message_words = min_message_words

    def process_item(self, item: DhOMessage, _):
        if self._is_too_short(msg=item.msg, min_words=self._min_message_words):
            raise DropItem
        return item

    @staticmethod
    def _is_too_short(msg: str, min_words: int) -> bool:
        n_words = len(msg.split())
        if n_words < min_words:
            return True
        return False
