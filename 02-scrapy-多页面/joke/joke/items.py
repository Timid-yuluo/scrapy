# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JokeItem(scrapy.Item):
    # define the fields for your item here like:

    # 约束传入的数据，多传就会报错
    ## 标题
    title = scrapy.Field()
    ## 内容
    content = scrapy.Field()


