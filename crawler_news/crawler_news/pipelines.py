# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from pymongo import MongoClient

class NoticiasPipeline(object):

    def open_spider(self, spider):
    	#...
    	self.connection = MongoClient('localhost', 27017)

    def close_spider(self, spider):
    	#...
      	""
    def process_item(self, item, spider):
      	#...
      	db = self.connection['news']
      	items =  db['itens']

      	query_find = itens.find({'id_news' : str(item['id_news'])})
      	if query_find:
      		print('Repeat!')
      	else:
      		items.insert_one({'title' : str(item['title']), 'link' : str(item['link']), 'time' : int(item['id_time']), 'id_news' : str(item['id_news']) })

      	return item

