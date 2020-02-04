# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    """

    """

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        """
        每个Item Pipeline类中必需实现process_item方法。会被自动调用
        当抓取到的text长度超过50则修改。低于50大于0则直接通过。等于0或未找到则抛弃此条Item
        :param item:
        :param spider:
        :return:
        """
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0: self.limit].rstrip() + "..."
            return item
        else:
            return DropItem("在该条Item中未找到有效的Text")


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """
        类方法。通过配置信息初始化mongodb的连接参数
        :param crawler:通过carwler可以拿到全局的配置信息。对应文件未settings.py文件。其中应该配置MONGO_URI和MONGO_DB
        :return:
        """
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        """
        当Spider被开启时此方法被调用
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        爬取结果写入数据库
        :param item:
        :param spider:
        :return:
        """
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        当Spider被关闭时此方法被调用
        :param spider:
        :return:
        """
        self.client.close()