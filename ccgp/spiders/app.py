# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ccgp.items import CcgpItem


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

        detail_list = response.xpath("//ul[@class='ulst']/li")
        for detail_li in detail_list:
            url = detail_li.xpath("./a/@href").extract()[0]
            item = CcgpItem()
            item['title'] = detail_li.xpath("./a/@title").extract()[0]
            item['publish_time'] = detail_li.xpath("./span[2]/text()").extract()[0]
            item['zone'] = detail_li.xpath("./span[3]/text()").extract()[0]
            request = scrapy.Request(urljoin_rfc(get_base_url(response), url), self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        item['content'] = response.xpath("//div[@class='vT_detail_content w760c']").extract()
        return item
