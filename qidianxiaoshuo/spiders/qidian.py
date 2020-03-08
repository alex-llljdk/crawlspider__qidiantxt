# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from qidianxiaoshuo.items import QidianxiaoshuoItem

#小说存储地址 C：/ruanjian/小说
class QidianSpider(CrawlSpider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com','book.qidian.com']
    start_urls = ['http://book.qidian.com/']

    rules = (
        Rule(LinkExtractor(allow="/info/\d+?", unique=True), callback='parse_book', follow=True),#爬取url规则
    )

    def parse_book(self, response):
        url = response.xpath(".//div[@class='book-detail-wrap center990']//a[@class='red-btn J-getJumpUrl ']/@href").get()
        url = response.urljoin(url)
        request = scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)
        yield request

    def parse_content(self, response):
        next_url = response.xpath(".//div[@class='wrap']//div[@class='chapter-control dib-wrap']/a[last()]/@href").get()
        next_url = response.urljoin(next_url)
        novel_name = response.xpath(".//div[@class='wrap']//div[@id='j_chapterBox']//div[@class='text-head']"
                                      "//div[@class='info fl']/a[1]/text()").get()
        chapter_name = response.xpath(".//div[@class='wrap']//div[@id='j_chapterBox']//div[@class='text-head']"
                                    "//h3/span/text()").get()
        contents = response.xpath("//div[@class='read-content j_readContent']/p/text()").getall()
        content=''
        for content1 in contents:
            content = content+content1+'\n'
        content.replace('\u3000','')
        item = QidianxiaoshuoItem(c_name=chapter_name, novel_name=novel_name,content = content)
        print("<<<<<<<" + item['novel_name'] + '  ' +
              item['c_name'] + "      爬取中<<<<<<<<<")
        if next_url:
            request = scrapy.Request(url=next_url, callback=self.parse_content, dont_filter=True)
            yield request
        yield item
        # chap_list = response.xpath(".//*[@class='listmain']/dl/dd")
        # novel_name = response.xpath(".//div[@id='book']//div[@id='info']/h1/text()").get()
        # for chapter in chap_list:
        #     c_name = chapter.xpath('./a/text()').get()
        #     c_url = chapter.xpath('./a/@href').get()
        #     if c_name:
        #         item = XiaoshuoItem(c_name=c_name, novel_name=novel_name)
        #         url = response.urljoin(c_url)
        #         request = scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)
        #         request.meta['key'] = item
        #         yield request
