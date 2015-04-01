# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc


class AppSpider(scrapy.Spider):
    name = "app"
    allowed_domains = ["ccgp.gov.cn"]
    start_urls = (
        'http://www.ccgp.gov.cn/cggg/dfgg/index.htm',
    )

    def parse(self, response):
        total, cur = re.search("Pager\(\{size:(\d+), current:(\d+), prefix:'index',suffix:'htm'\}\);", response.body).groups()
        if int(cur) < int(total):
            next_page = "http://www.ccgp.gov.cn/cggg/dfgg/index_%d.htm" % (int(cur) + 1)
            yield scrapy.Request(next_page)

        details = response.xpath("//ul[@class='ulst']/li/a/@href").extract()
        for detail in details:
            yield scrapy.Request(urljoin_rfc(get_base_url(response), detail), self.parse_detail)

    def parse_detail(self, response):
        title, = response.xpath("//h2[@class='tc']/text()").extract()
        print title
