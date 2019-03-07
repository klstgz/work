# -*- coding: utf-8 -*-
# encoding=utf-8
import sys
from govtest.items import GovtestItem

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy


class GovSpider(scrapy.Spider):
    name = 'gov'
    # allowed_domains = ['gov.cn']
    a = []
    for i in range(310):
        b = 'http://sousuo.gov.cn/column/31250/{}.htm'.format(i)
        a.append(b)
    start_urls = a

    def parse(self, response):
        li_list = response.xpath('//div[2]/div/div[2]/div[2]/ul/li/h4/a')
        for li in li_list:
            url = li.xpath('.//@href').extract_first()
            # print url
            yield scrapy.Request(url, callback=self.parse_a)

    def parse_a(self, response):

        url = response.url
        time = response.xpath('normalize-space(//div[@class="pages-date"]/text())').extract_first()
        title_list = response.xpath('normalize-space(//h1/text())').extract()
        text_list = response.xpath('//body//p/text()').extract()
        title = ''.join(title_list)
        text = '\n'.join(text_list)
        item = GovtestItem()
        item['url'] = url
        item['time'] = time
        item['title'] = title
        item['text'] = text
        print('--' * 20)
        yield item
