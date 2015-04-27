# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import urllib
import traceback
from StringIO import StringIO
from urlparse import urljoin

import redis
import torndb
import requests
from pyquery import PyQuery as _Q

from ccgp import vcode


class CcgpPipeline(object):
    def __init__(self, settings):
        self.redis = redis.Redis(**settings.get('REDIS'))
        self.db = torndb.Connection(**settings.get('DATABASE'))
        self.settings = settings

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def process_item(self, item, spider):
        self.db.execute("start transaction")
        if not self.redis.sismember('base', item['url']):
            cnt = _Q(item['content'])
            for t in cnt('table'):
                if t.attrib.get('width'):
                    t.set('width', '')
            for n in cnt("*"):
                if t.attrib.get('style'):
                    t.set('style', '')
            item['content'] = str(cnt)
            base_id = self.db.insert("insert into base(category, url, title, zone, content, publish_time, source, sn) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                                     item['category'], item['url'], item['title'], item['zone'], item['content'], item['publish_time'], item['source'], item['sn'])
            if base_id:
                try:
                    for atts in item['attachments']:
                        if 'documentView.do?method=downFile' in atts['url']:
                            session = requests.Session()
                            response = session.get(atts['url'])
                            q = _Q(response.content)
                            params = {}
                            for i in q("form input"):
                                if i.name:
                                    params[i.name] = i.value

                            img_url = q('form img').attr('src')
                            response = session.get(urljoin("http://www.cqgp.gov.cn/", img_url))
                            imgio = StringIO(response.content)
                            params['imageString'] = vcode.analyze(imgio)

                            post_url = q('form').attr('action')
                            response = session.post(urljoin("http://www.cqgp.gov.cn/", post_url), data=params)
                            filename = re.search('attachment; filename="(.*?)"',
                                                 response.headers['content-disposition']).group(1)
                            filename = urllib.unquote(filename)
                            self.db.insert("insert into attachments(url, base_id, name, file) values(%s, %s, %s, %s)",
                                           atts['url'], base_id, filename, torndb.MySQLdb.Binary(response.content))
                        else:
                            headers = self.settings.get("DEFAULT_REQUEST_HEADERS")
                            headers['Referer'] = item['url']
                            if item['source'] == u'惠州市公共资源交易中心':
                                headers['Host'] = '183.63.34.151:8888'
                                session = requests.Session()
                                session.headers = headers
                                session.get(item['url'])
                                response = session.get(atts['url'])
                                try:
                                    filename = re.search('attachment; filename=(.*?)',
                                                         response.headers['content-disposition']).group(1)
                                    atts['name'] = urllib.unquote(filename)
                                except:
                                    continue
                            else:
                                response = requests.get(atts['url'], headers=headers)
                            self.db.insert("insert into attachments(url, base_id, name, file) values(%s, %s, %s, %s)",
                                           atts['url'], base_id, atts['name'], torndb.MySQLdb.Binary(response.content))
                except Exception as e:
                    traceback.print_exc()
                    self.db.execute("rollback")
                else:
                    self.db.execute("commit")
                    self.redis.sadd('base', item['url'])
            return item['title']
