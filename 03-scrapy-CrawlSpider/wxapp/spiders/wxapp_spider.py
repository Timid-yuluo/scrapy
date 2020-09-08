# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        # .+ 和 /d 用正则,设置满足条件的url
        # follow=True,表示一直跟进，当网页翻页后，在翻页后的页面寻找满足条件的url（即符合allow中设置的url规则）
        # 为False则只保存第一个页面满足的url
        ## 主页面需要的url示范： http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=/d'), follow=True),

        # 详情页面需要回调，（回调后解析内容，保存），且不需要跟进
        ## 详情页面需要的url示范 http://www.wxapp-union.com/article-5822-1.html
        ### \. 转义字符
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), follow=False, callback="parse_detail"),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        author = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[3]/div[1]/p/a/text()').get()
        time = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[3]/div[1]/p/span/text()').get()
        # print(title + '\n' + author + ' ' +  time)
        # print('='*30)
        article_content = response.xpath('//*[@id="article_content"]//text()').getall()
        article_content = "".join(article_content).strip()
        # print(article_content)
        item = WxappItem()
        item['title'] = title
        item['author'] = author
        item['time'] = time
        item['article_content'] = article_content
        yield item




'''1.CrawlSpider与普通爬虫的区别是，CrawlSpider根据正则匹配规则，自动找符合规则的页面(自动翻页)
'''

'''2.主页面就是控制页码的1,2,3,4，，，n页
   详情页面是主页面中的一些可点击的文字(如标题)等，点击后会跳转到另一个页面，里面有很多内容
   而我们往往需要详情页面的内容,需要获取数据的都需要回调
'''

'''3.详情页面不需要跟进，主页面相当于翻页，详情页相当于读取内容，
   在详情页中跳转到其他页面，会与主页面的翻页造成冲突
'''
