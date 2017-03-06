# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
from .items import CampusTalkItem, ShuangXuanHui, ZhaoPinGonGao


class JobinfoPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        userName = settings['MONGODB_USERNAME']
        password = settings['MONGODB_PASSWORD']
        client = pymongo.MongoClient(host=host, port=port)
        pymongo.MongoClient()
        self.tdb = client[dbName]
        self.tdb.authenticate(name=userName, password=password)

    def process_item(self, item, spider):
        if isinstance(item, CampusTalkItem) is True:
            self.post = self.tdb['CampusTalkItem']
        elif isinstance(item, ShuangXuanHui) is True:
            self.post = self.tdb['ShuangXuanHui']
        else:
            self.post = self.tdb['ZhaoPinGonGao']
        if self.post.find({"name": item["name"], "date": item["date"]}).count() == 0:
            info = dict(item)
            self.post.insert(info)
        # print item
        return item
