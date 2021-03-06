import pymongo
from pymongo import MongoClient

#Class for handle MongoAccess
class MongoStore(object):
	def __init__(self):
		self.connection = MongoClient('localhost', 27017)
		self._db = self.connection['news']

	#	--------------	
	#	CRUD FUNCTIONS
	#	--------------

	def put(self, msg):
		users = self._db['users']

		chat_id = msg['chat']['id']

		users_list = []
		for user in users.find():
			users_list.append(user['chat_id'])
		if chat_id not in users_list:
			users.insert_one({"chat_id": chat_id, "messages" : [msg] })

		users.update_one({"chat_id" : chat_id}, {"$push" : {"messages" : msg} })

	# Pull all unread messages of a `chat_id`
	def pull(self, chat_id):
		users = self._db['users']

		results = users.find({"chat_id" : chat_id})

		messages = []
		for result in results:
			messages.append(result['messages'])

		return messages

	#Function to return all users using stocks bot
	def getUsers(self):
		users = self._db['users']

		results = users.find()

		chats_id = []
		for result in results:
			chats_id.append( int(result['chat_id']) )

		return chats_id


	#	--------------	
	#	NEWS FUNCTIONS
	#	--------------


	#Function to return last items in mongo db news collections	
	def getLastItems(self, count):
		connection = MongoClient('localhost', 27017)
		
		db = connection['news']
		itens =  db['itens']

		query_find = itens.find().sort([("time", pymongo.DESCENDING)])

		items = []
		for result in query_find:
			item = "News: "+result['title']+"/nlink: "+result['link'] 

			items.append(item)
		if count > 0:
			return items[:count]
		else :
			return items[:10]
