# coding:utf-8
import scrapy

from scrapy.crawler import CrawlerProcess


from tkphoto.items import TkphotoItem


class TkphotoSpider(scrapy.Spider):

    name = 'tkphoto'
    allowed_domains = []
    start_urls = ["http://tkofficial.jp/photologs/"]

    # 1.从tkofficial/photolog/提取所有博客文章链接，保存标题
    # 2.打开所有博客文章链接，将其中的图片链接放入下载队列
    # 3.下载大图（pipelines.py）
    def parse(self, response):
        items = []
        allblogs = response.xpath('//div[@class="thumBox"]/a/@href').extract()  # 提取blog地址链接
        for blogurl in allblogs:
            item = TkphotoItem()
            item['blog_url']=blogurl
            items.append(item)
        for item in items:
            yield scrapy.Request(item['blog_url'], callback=self.blogparse, meta={'item_1': item})

        # item = TkphotoItem()
        # item['image_link'] = response.xpath('//div[@class="thumBox"]/a/@href').extract()  # 提取blog地址链接
        # print '*************************************'
        # print 'image_urls',item['image_link']
        # for url in item['image_link']:
        #     print '----------------------------------'
        #     liststring = url.split('/')
        #     item['image_name'] = liststring[len(liststring)-2]
        #     yield scrapy.Request(url, callback=self.blogparse, meta={'item':item})
        #yield item

        new_url = response.xpath('//p[@class="prevBtn"]/a/@href').extract_first()  # 翻页
        # print 'new_url',new_url
        if new_url:
            yield scrapy.Request(new_url, callback=self.parse)

    # 第二层的网页提取：blog页提取其他信息
    def blogparse(self,response):
        item_1 = response.meta['item_1']
        item = TkphotoItem()
        downlink=[]
        downlink = response.xpath('//div[@class="photolog"]//img/@src').extract()  # blog的大图地址提取
        # 查错用if  长时间没用之后发现是xpath规则无效，此时可使用scrapy shell进行尝试和修改
        if(downlink==[]):
            print "downloadlink is null"
        else:
            item['blog_piclink']=downlink[0]
        time = response.xpath('//div[@class="photolog"]//p[@class="pageDate"]/text()').extract()  # 时间提取
        print time
        item['blog_time']=time[0]
        name = response.xpath('//div[@class="photolog"]//p[@class="pageTit"]/text()').extract()  # 标题提取
        item['blog_name'] = name[0]
        print name
        content = response.xpath('//div[@class="photolog"]//div[@class="pageConts"]/p/text()').extract()  # 内容提取
        item['blog_content'] = content
        item['blog_url']=item_1['blog_url']
        print item['blog_name']
        yield item

