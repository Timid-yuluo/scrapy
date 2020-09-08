# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
# 导入items中的类
from joke.items import JokeItem
# 该代码只负责解析
class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohua.zol.com.cn/']
    start_urls = ['http://xiaohua.zol.com.cn//']

    def parse(self, response):
        # response是 scrapy.http.response.html.HtmlResponse 对象可执行xpath和css语法
        ## 需导包from scrapy.http.response.html import HtmlResponse
        jokes = response.xpath('//ul[@class="news-list video-list"]/li/a')
        # print('---------', jokes)
        for joke in jokes:
            title = joke.xpath('./@title')[0].extract()
            # 后面的xpath只获得域名
            href = 'http://xiaohua.zol.com.cn/' + joke.xpath('./@href').get()
            # print('----------',title,href)
            item = JokeItem()
            item['title'] = title
            item['href'] = href
            # 把数据返回给pipelines
            yield item