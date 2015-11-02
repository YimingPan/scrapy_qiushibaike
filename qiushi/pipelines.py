# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class QiushiPipeline(object):
    def __init__(self):
        self.fileSql = open(u'items.sql', u'wb')

    def process_item(self, item, spider):
        #print item['content']
        #print item['title']
        data = dict(item)
        sqlAuthor = u"INSERT INTO tbl_user (username, passwd, nickname, salt) VALUES ('system_糗事百科', 'nologin', '糗事百科', 'nologin');"
        sqlNews = u"INSERT INTO tbl_news (title, category_id, content, author_id) VALUES ('{title}', (select id from tbl_category where name='段子'), '{content}', (select id from tbl_user where username='system_糗事百科'));".format(**data)
        line = sqlAuthor + u'\n' + sqlNews + u'\n'
        self.fileSql.write(line)

        return item
