import pymongo
from pymongo import MongoClient
import models

def getLastItems():
	connection = MongoClient('localhost', 27017)
	
	db = connection['news']
	itens =  db['itens']

	query_find = itens.find().sort([("time", pymongo.DESCENDING)])

	items = []
	for result in query_find:
		item = "News: "+result['title']+"/nlink: "+result['link'] 

		items.append(item)

	return items[:10]		