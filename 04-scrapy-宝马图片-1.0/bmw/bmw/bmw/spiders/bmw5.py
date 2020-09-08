# -*- coding: utf-8 -*-
import scrapy
from ..items import BmwItem

class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    # 限制网址域名，若爬取的网址域名改变，则会爬取不成功（就得注释该语句）
    allowed_domains = ['car.autohome.com.cn']
    # 默认网址
    # start_urls = ['http://car.autohome.com.cn/']
    # 把默认网址改为要爬取的网址
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        # 第一个（index[0]）不需要
        uiboxs = response.xpath('.//div[@class="column grid-16"]/div[@class="uibox"]')[1:]
        for uibox in uiboxs:
            # get获取第一个
            title = uibox.xpath('./div[@class="uibox-title"]/a/text()').get()
            # print(title)

            # 获得所有，封装成列表,但里面的url缺少域名
            urls = uibox.xpath('.//ul/li/a/img/@src').getall()
            # 1.遍历元素，添加域名，最终为单个元素
            # for url in urls:
            #     url = 'https:' + url
            #     # 或者根据域名自动拼接网址
            #     # url = response.urljoin(url)
            #     print(url)

            # 2.使用map方法，且把生成的元素封装成列表
            ## 传入列表（urls），遍历列表中的每个元素，
            ## 每遍历一个元素就调用匿名函数，执行语句（response.urljoin(url)）
            urls = list(map(lambda url:response.urljoin(url),urls))

            # 传入管道,items 中加title = scrapy.Field()，urls = scrapy.Field()
            item = BmwItem(title=title, urls=urls)
            yield item


