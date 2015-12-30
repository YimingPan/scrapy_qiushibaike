# -*- coding: utf-8 -*-
import scrapy
from qiushi.items import DuanziItem
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class DuanziSpider(scrapy.Spider):
    name = "Duanzi"
    allowed_domains = ["qiushibaike.com"]
    headers = {
        'Referer' : 'http://www.qiushibaike.com/text',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    
    def start_requests(self):
        # 爬取糗事百科上最新文字版块的全部35个页面
        requestlist = []
        for i in range(1, 36):
            url = "http://www.qiushibaike.com/textnew/page/%d?s=4835373" % i
            requestlist.append(scrapy.FormRequest(url, headers = self.headers))
        return requestlist

    def parse(self, response):
        data = response.xpath('//div[@class="article block untagged mb15"]')
        for duanzi in data:
            item = DuanziItem()
            content = duanzi.xpath('div[@class="content"]/text()').extract()
            author = duanzi.xpath('div[@class="author clearfix"]/a/h2/text()').extract()

            # 有些用户没有用户名，不知是什么原因。过滤掉这些段子。
            if author == []:
                continue

            # 糗事百科上的正文内容经常含'<br>'，导致正文被割裂成若干个列表元素。
            # 将他们逐一提取出来，连接之后再存入content域。
            t = ''
            for text in content:
                if text != '\n':
                    t = t + text.replace('\n', '') + '\n'
            item['content'] = t
            item['author'] = author[0]

            # 获取评论页面的链接
            comment_page = duanzi.css('ul.clearfix > li.comments > a::attr("href")').extract()
            url = response.urljoin(comment_page[0])
            item['href'] = url;
            request = scrapy.Request(url, headers=self.headers, callback=self.parse_title)
            request.meta['item'] = item

            yield request

    def parse_title(self, response):
        item = response.meta['item']
        item['title'] = response.css('title::text').extract()[0].replace('\n', '')

        return item
