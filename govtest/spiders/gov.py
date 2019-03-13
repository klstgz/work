# -*- coding: utf-8 -*-
import sys
from govtest.items import GovtestItem
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import requests



class GovSpider(scrapy.Spider):
    name = 'gov'
    # allowed_domains = ['gov.cn']

    # 获取页数
    html = requests.get('http://sousuo.gov.cn/column/31250/0.htm')
    html.encoding = "utf-8"
    selecter = etree.HTML(html.text)
    s = str(selecter.xpath('//*[@id="toPage"]/li[1]/text()')[0])
    page=re.sub("\D", "", s)
    page=int(page)

    # 创建爬取队列
    a = []
    for i in range(page):
        b = 'http://sousuo.gov.cn/column/31250/{}.htm'.format(i)
        a.append(b)
    start_urls = a
    # 爬虫1
    def parse(self, response):
        li_list = response.xpath('//div[2]/div/div[2]/div[2]/ul/li/h4/a')
        for li in li_list:
            url = li.xpath('.//@href').extract_first()
            # print url
            yield scrapy.Request(url, callback=self.parse_a)
    # 爬虫2
    def parse_a(self, response):

        next1 = response.xpath('//p/img/@src').extract()
        img_list = []
        for next in next1:
            next_url = response.urljoin(next)
            img_list.append(next_url)


        url = response.url
        time = response.xpath('normalize-space(//div[@class="pages-date"]/text())').extract_first()
        title_list = response.xpath('//h1/text()').extract()
        text_list = response.xpath('//body//p/text()').extract()

        title = ''.join(title_list)
        text = '\n'.join(text_list)
        image = '##'.join(img_list)
        # 传递
        item = GovtestItem()
        item['url'] = url
        item['time'] = time
        item['title'] = title
        item['text'] = text
        item['image']=image
        print('--' * 20)
        print image
        yield item
