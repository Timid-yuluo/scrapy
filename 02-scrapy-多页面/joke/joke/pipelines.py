# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json # 自行导入需要的库

class JokePipeline(object):
    def __init__(self):
        self.fp = open(r'C:\Users\ASUS PC\Desktop\joke.txt', mode='a', encoding='utf-8')

    def open_spider(self,spider):
        print('爬虫开始-----------')

    def process_item(self, item, spider):
        # 把传来的数据改为dict 再转化为json数据（直接写入dict会报错）
        ## ensure_ascii=False 解决乱码
        # item_json = json.dumps(dict(item), ensure_ascii=False)
        # self.fp.write(item_json + '\n')

        # 不使用json格式数据，不需要导json库
        self.fp.write('%s%s'%(item['title'],item['content']))
        # 处理数据后，传给下一个管道
        return item

    def close_spider(self,spider):
        self.fp.close()
        print('爬虫结束-----------')

