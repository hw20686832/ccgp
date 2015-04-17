# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CcgpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    zone = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    attachments = scrapy.Field()
    source = scrapy.Field()
    group = scrapy.Field()
    sn = scrapy.Field()

    def __str__(self):
        return self['title']
