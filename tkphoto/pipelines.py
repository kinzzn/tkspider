# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib

from scrapy import log
from scrapy.exceptions import DropItem

from tkphoto import settings

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from pymongo import MongoClient

class TkphotoPipeline(object):

    def __init__(self):
        client = MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = client[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Insert %s"%item['blog_name'])

        # 下载图片到本地(去掉注释可用)
        # dir_path = '%s'%(settings.IMAGES_STORE)
        # print 'dir_path',dir_path,' type:',type(dir_path)
        # if not os.path.exists(dir_path):
        #     os.makedirs(dir_path)
        # file_name = item['blog_name']  # 图片名称
        # if file_name.replace('\\','-')==True:
        #     print 'got \\'
        # file_name=file_name.encode('gbk','replace')+'.jpg'
        # print 'type blogname',type(item['blog_name'])   # 文件下载时的类型应该根据下载链接的类型决定，判断应该改为.split得到list最后一个
        # file_path = '%s/%s' % (dir_path, file_name) #,item['blog_piclink'][len(item['blog_piclink'])-4:len(item['blog_piclink'])])
        # if os.path.exists(file_name):
        #     pass
        # with open(file_path, 'wb') as file_writer:
        #     conn = urllib.urlopen(item['blog_piclink'])  # 下载图片
        #     file_writer.write(conn.read())
        # file_writer.close()

        return item
