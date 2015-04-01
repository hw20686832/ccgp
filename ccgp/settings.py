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
#USER_AGENT = 'ccgp (+http://www.yourdomain.com)'
ITEM_PIPELINES = {'ccgp.pipelines.CcgpPipeline': 300}

REDIS = {'host': 'localhost', 'port': 6379, 
         'db': 0}

DATABASE = {'host': 'localhost', 'database': 'admin', 
            'user': 'admin', 'password': '1qa2ws#ed'}
