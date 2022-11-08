# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from bs4 import BeautifulSoup

from itemadapter import ItemAdapter


class RemoveBlockquotesPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['msg'] = self._remove_blockquotes(adapter['msg'])
        return item

    @staticmethod
    def _remove_blockquotes(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.findAll('div', class_='quote'):
            tag.decompose()
        return str(soup)
