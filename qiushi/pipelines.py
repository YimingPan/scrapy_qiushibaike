# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QiushiPipeline(object):
    def process_item(self, item, spider):
        print "Author: %s" % item['author']
        #print "Title: %s" % item['title']
        for com in item['comment']:
            print com
        return item
