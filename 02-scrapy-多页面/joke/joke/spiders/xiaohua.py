# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
# 导入items中的类
from joke.items import JokeItem
# 该代码只负责解析
class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    # 限制爬虫的范围，
    ## 如果xiaohua.zol.com.cn/lengxiaohua/后面还有其他字符组建成新网址，则会访问不到
    ## 如下面的调度，self.base_url+next_page
    # allowed_domains = ['xiaohua.zol.com.cn/lengxiaohua/']
    start_urls = ['http://xiaohua.zol.com.cn/lengxiaohua/']
    # 用于翻页
    base_url = 'http://xiaohua.zol.com.cn'

    def parse(self, response):
        # response是 scrapy.http.response.html.HtmlResponse 对象可执行xpath和css语法
        ## 需导包from scrapy.http.response.html import HtmlResponse
        jokes = response.xpath('//ul[@class="article-list"]/li')
        for joke in jokes:
            title = joke.xpath('./span[2]/a/text()')[0].extract()
            # print(title)
            content = joke.xpath('./div[2]//text()').extract()
            # content是列表，且有很多无效字符
            ## 把字符串连接起来且消除\t,\n字符
            content = " ".join(content).replace('\t','').replace('\n','')
            # print(content)
            item = JokeItem()
            item['title'] = title
            item['content'] = content
            # 把数据返回给pipelines,用return会结束函数
            yield item
        # 获取下一页的链接，get可取出（用法与xpath有点不一样）
        next_page = response.xpath('//div[@class="page-box"]/div/a[@class="page-next"]/@href').get()
        print('----------------',next_page)
        print(self.base_url+next_page)
        # 请求下一页的网址，callback调用parse函数，实现循环
        yield scrapy.Request(self.base_url+next_page, callback=self.parse)