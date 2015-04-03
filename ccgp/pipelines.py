# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import torndb
import requests


class CcgpPipeline(object):
    def __init__(self, settings):
        self.redis = redis.Redis(**settings.get('REDIS'))
        self.db = torndb.Connection(**settings.get('DATABASE'))

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        if not self.redis.sismember('base', item['url']):
            base_id = self.db.insert("insert into base(url, title, zone, content, publish_time) values(%s, %s, %s, %s, %s)",
                                     item['url'], item['title'].encode('utf-8'), item['zone'].encode('utf-8'), item['content'].encode('utf-8'), item['publish_time'])
            if base_id:
                for atts in item['attachments']:
                    response = requests.get(atts['url'])
                    self.db.insert("insert into attachments(url, base_id, name, file) values(%s, %s, %s, %s)",
                                   atts['url'], base_id, atts['name'].encode('utf-8'), torndb.MySQLdb.Binary(response.content))

            self.redis.sadd('base', item['url'])
            return base_id
