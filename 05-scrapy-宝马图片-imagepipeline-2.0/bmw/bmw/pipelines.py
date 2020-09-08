# -*- coding: utf-8 -*-

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request

# 启动pipelines，需要在settings取消注释（68行）
class BmwPipeline(object):
    def __init__(self):
        # 参见实战中 教程-2.0-os模块
        # 在当前路径的上一级目录中，查找images目录
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')

        # 判断是否有images目录，没有则创建
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        # 取出item中的数据
        title = item['title']
        urls = item['urls']

        # title 有 车身外观，中控方向盘等
        # 在images文件夹中创建以title为名的文件夹
        title_path = os.path.join(self.path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)

        for url in urls:
            # 设置图片的的名字，取url中 _ 后面字符串为图片名
            # url示例
            # https://car3.autoimg.cn/cardfs/product/g3/M08/5D/99/240x180_0_q95_c42_autohomecar__ChcCRV2J-teAYMC3AAah0O0frSA485.jpg
            image_name = url.split('_')[-1]
            # request.urlretrieve 方法能把图片地址保存为图片
            # 后面设置文件保存的路径，和文件名
            request.urlretrieve(url, os.path.join(title_path, image_name))
        return item
