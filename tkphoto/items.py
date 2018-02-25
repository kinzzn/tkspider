# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TkphotoItem(scrapy.Item):
    # define the fields for your item here like:
    # 一个图片下载链接，一个名字，一个时间，一个链接，一段文字
    blog_url = scrapy.Field()
    blog_name = scrapy.Field()
    blog_time = scrapy.Field()
    blog_piclink = scrapy.Field()
    blog_content = scrapy.Field()
