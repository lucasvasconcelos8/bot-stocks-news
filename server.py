import flask
from flask import Flask
import markdown

app = Flask(__name__)

import telepot


TelegramBot = telepot.Bot("650006953:AAHp3VTA6sGuYFQhvljN7ekZgZ59N4vZBzY")

##test lixo
import pymongo
from pymongo import MongoClient

def getLastItens():
	connection = MongoClient('localhost', 27017)
	
	db = connection['news']
	itens =  db['itens']

	query_find = itens.find().sort([("time", pymongo.DESCENDING)])

	items = []
	for result in query_find:
		item = "News: "+result['title']+"/nlink: "+result['link'] 

		items.append(item)

	return items[:10]

@app.route("/feed")
def getLast():
	content = markdown.markdown(str(getLastItens()))
	TelegramBot.sendMessage(chat_id = int(154420266), text = content , parse_mode='Markdown')
	return ""