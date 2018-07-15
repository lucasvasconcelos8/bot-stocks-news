# -*- coding: utf-8 -*-
import scrapy
import time
from crawler_news.items import NoticiasItem

class InfomoneySpider(scrapy.Spider):
    name = 'infoMoney'
    allowed_domains = ['infomoney.com.br/']
    start_urls = ['http://infomoney.com.br/']

    def parse(self, response):
    	#response.css("a.title-box").css("::attr(href)").extract_first()
      for news in response.css("a.title-box"):
        link    = news.css("::attr(href)").extract_first()
        title   = news.css("::text").extract_first()

        #timestamp for news
        ts = int(time.time())

        #id_news for infomoney case
        id_news = str(link).split('/')[-1]
        print(id_news)

        notice = NoticiasItem(title=title, link=self.start_urls[0][:-1]+link, id_time=ts, id_news=id_news)
        yield notice
