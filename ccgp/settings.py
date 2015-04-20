# -*- coding: utf-8 -*-

# Scrapy settings for ccgp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ccgp'

SPIDER_MODULES = ['ccgp.spiders']
NEWSPIDER_MODULE = 'ccgp.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = '"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                           "Accept-Encoding": "gzip, deflate, sdch",
                           "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ar;q=0.2",
                           "Cache-Control": "max-age=0",
                           "Connection": "keep-alive",
                           #"Host": "www.dianping.com",
                           #"Referer": "http://www.dianping.com/",
                           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36"}

ITEM_PIPELINES = {'ccgp.pipelines.CcgpPipeline': 300}

REDIS = {'host': 'localhost', 'port': 6379,
         'db': 0}

DATABASE = {'host': 'localhost', 'database': 'admin',
            'user': 'admin', 'password': '1qa2ws#ed'}
