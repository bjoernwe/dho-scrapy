# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from pydantic import BaseModel


class DhOMessage(BaseModel):
    title: str
    msg: str
