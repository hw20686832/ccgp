# -*- coding: utf-8 -*-
import re
import datetime

import scrapy
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from pyquery import PyQuery as _Q

from ccgp.items import CcgpItem


class AppSpider(scrapy.Spider):
    name = "app"
    allowed_domains = ["ccgp.gov.cn"]
    start_urls = (
        'http://www.ccgp.gov.cn/cggg/dfgg/index.htm',
        'http://www.ccgp.gov.cn/cggg/zygg/index.htm'
    )
    group_1 = (979, 1001, 974, 998, 976, 996, 978, 1000, 977, 999, 984, 1006, 985, 1007, 975, 997)
    group_2 = (982, 1004, 981, 1003, 990, 1012)

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
            # item['publish_time'] = detail_li.xpath("./span[2]/text()").extract()[0]
            item['publish_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['zone'] = detail_li.xpath("./span[3]/text()").extract()[0]
            item['category'] = int(detail_li.xpath("./span[1]/text()").extract()[0])
            if item['category'] in self.group_1:
                item['group'] = 0
            else:
                item['group'] = 1
            request = scrapy.Request(urljoin_rfc(get_base_url(response), url), self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        q = _Q(response.body_as_unicode())
        content = q('div.vT_detail_content.w760c').text()
        item = response.meta['item']
        item['url'] = response.url
        item['content'] = response.xpath("//div[@class='vT_detail_content w760c']").extract()[0]
        item['source'] = u'中国政府采购网'
        try:
            item['sn'] = re.search(u".*编号：\s?(.*?)[\s|；|;|,|\.|，|。|<|\]|］|\)|）]", content).group(1)
        except:
            item['sn'] = ''
        attachments = []
        atts = response.xpath(
            "//a[contains(@href, '.doc') or contains(@href, '.pdf') or contains(@href, '.zip') or contains(@href, '.rar') or contains(@href, '/documentView.do?method=downFile')]")
        for att in atts:
            attach = {}
            att_url = att.xpath("./@href").extract()[0]
            try:
                url = urljoin_rfc("http://cpms.ccgp.gov.cn", att_url[att_url.index('/UploadFiles'):])
            except:
                url = att_url
                if att_url.startswith('/gdgpms'):
                    url = urljoin_rfc("http://www.gdgpo.gov.cn/", att_url)
                if att_url.startswith('/henan/rootfiles'):
                    url = urljoin_rfc("http://www.hngp.gov.cn/", att_url)
                if att_url.startswith('/jiaozuo/rootfiles'):
                    url = urljoin_rfc("http://www.hngp.gov.cn/", att_url)
                if att_url.startswith('/shangqiu/rootfiles'):
                    url = urljoin_rfc("http://www.hngp.gov.cn/", att_url)

            attach['url'] = urljoin_rfc("http://www.gdgpo.gov.cn/", url)
            if "bulletin_zz.do?method=downloadFile" in attach['url']:
                attach['name'] = re.search("&file_name=(.*)$", attach['url']).group(1)
            else:
                attach['name'] = attach['url'].rsplit('/', 1)[1]
            attachments.append(attach)
        item['attachments'] = attachments
        return item
