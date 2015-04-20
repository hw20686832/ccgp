# -*- coding: utf-8 -*-
import re
import datetime
import urlparse

import scrapy
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ccgp.items import CcgpItem


class HuizhouSpider(scrapy.Spider):
    name = "huizhou"
    allowed_domains = ["ccgp.gov.cn"]
    start_urls = (
        'http://zyjy.huizhou.gov.cn/pages/cms/hzggzyjyzx/html/artList.html?cataId=11d8ed160d2e437590964a4c47db8cfe',
    )

    cate_map = {'d1906435886c4ee188887bc8297606ed': 990,
                'cd8722228cfc49f384c6b7abcf34cee0': 982,
                'f304ef72299e4c42a84077a7707f4caa': 981}

    def parse(self, response):
        next_page = response.xpath(u"//a[contains(text(), '下一页')]/@href").extract()
        if next_page:
            yield scrapy.Request(urljoin_rfc(get_base_url(response), next_page[0]))
        alist = response.xpath("//td[@id='div_list']/ul[@class='ul_art_row']/li[@class='li_art_title']/a/@href").extract()
        for a in alist:
            yield scrapy.Request(urljoin_rfc(get_base_url(response), a), callback=self.parse_detail)

    def parse_detail(self, response):
        item = CcgpItem()
        item['url'] = response.url
        item['title'], = response.xpath("//td[@class='artTitle']/text()").extract()
        item['publish_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['zone'] = u"惠州"
        item['source'] = u'惠州市公共资源交易中心'
        item['content'] = response.xpath("//td[@class='artContent']/*").extract()[0]
        cate_id = urlparse.urlparse(response.url).query.split('=')[1]
        item['category'] = self.cate_map[cate_id]
        item['group'] = 'group_2'
        try:
            item['sn'] = re.search(u".*编号：\s?(.*?)[\s|；|;|,|\.|，|。|<|\]|］|\)|）]", content).group(1)
        except:
            item['sn'] = ''

        attachments = []
        atts = response.xpath("//a[contains(@href, '183.63.34.151:8888/hp/project')]/@href").extract()
        for att in atts:
            attach = {}
            attach['url'] = att
            attach['name'] = ''
            attachments.append(attach)

        item['attachments'] = attachments
        return item
