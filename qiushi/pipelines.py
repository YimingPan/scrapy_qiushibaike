# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from datetime import date
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class QiushiPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # The file created on Dec20 2015 will be named as "12-20-2015.json"
        datestr = date.today().strftime("%m-%d-%Y")
        file = open('scraped_data/%s.json' % datestr, 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # print item['author']
        # print item['title']
        # print item['content']
        # print item['href']

        return item
