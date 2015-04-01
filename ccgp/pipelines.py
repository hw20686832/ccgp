# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import torndb


class CcgpPipeline(object):
    def __init__(self, settings):
        self.redis = redis.Redis(**settings.get('REDIS'))
        self.db = torndb.Connection(**settings.get('DATABASE'))

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        rs = self.db.insert("insert into base(title, zone, content, publish_time) values(%s, %s, %s, %s)", 
                       item['title'], item['zone'], item['content'], item['publish_time'])
        return rs
