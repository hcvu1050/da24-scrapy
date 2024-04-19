# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Project1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field ()
    category = scrapy.Field()
    author_name = scrapy.Field()
    author_email = scrapy.Field()
    publish_date = scrapy.Field()
    