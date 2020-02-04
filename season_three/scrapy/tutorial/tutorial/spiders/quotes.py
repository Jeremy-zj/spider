# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 使用css选择器得到所有样式为quote的元素
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        
        # 得到下一页的url
        next = response.css('.pager .next a::attr("href")').extract_first()
        # 得到url
        url = response.urljoin(next)
        # 指定下一页的地址和回调函数
        yield scrapy.Request(url=url, callback=self.parse)
