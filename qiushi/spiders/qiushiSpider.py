# -*- coding: utf-8 -*-
import scrapy
from qiushi.items import DuanziItem


class DuanziSpider(scrapy.Spider):
    name = "Duanzi"
    allowed_domains = ["qiushibaike.com"]
    headers = {
        'Referer' : 'http://www.qiushibaike.com/text',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    
    def start_requests(self):
        return [scrapy.FormRequest("http://www.qiushibaike.com/textnew",
                                    headers=self.headers)]

    def parse(self, response):
        data = response.xpath('//div[@class="article block untagged mb15"]')
        for duanzi in data:
            item = DuanziItem()
            content = duanzi.xpath('div[@class="content"]/text()').extract()
            author = duanzi.xpath('div[@class="author"]/a/text()').extract()

            if author == []:
                continue

            item['content'] = '<div class="content">\n' + content[0].replace('\n', '') + '\n</div>'
            item['author'] = author[1].replace('\n', '')

            # 获取评论页面的链接
            comment_page = duanzi.css('ul.clearfix > li.comments > a::attr("href")').extract()
            url = response.urljoin(comment_page[0])
            request = scrapy.Request(url, headers=self.headers, callback=self.parse_title)
            request.meta['item'] = item

            yield request

    def parse_title(self, response):
        item = response.meta['item']
        item['title'] = response.css('title::text').extract()[0].replace('\n', '')
        # item['comment'] = response.xpath('//span[@class="body"]/text()').extract()
        return item
