import sys
import time
import telepot
import pymongo
from pymongo import MongoClient
from repository import getLastItems
import asyncio
from telepot.loop import MessageLoop
from telepot.delegate import (
    per_chat_id_in, per_application, call, create_open, pave_event_space)

class MongoStore(object):
	def __init__(self):
		self.connection = MongoClient('localhost', 27017)
		self._db = self.connection['news']

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

	# Tells how many unread messages per chat_id
	def unread_per_chat(self):
		return ["007"]


# Accept commands from owner. Give him unread messages.
class CommandsHandler(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, store, **kwargs):
        super(CommandsHandler, self).__init__(seed_tuple, **kwargs)
        self._store = store

    def _read_messages(self, messages):
        for msg in messages:
            # assume all messages are text
            self.sender.sendMessage(msg['text'])

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.sender.sendMessage("I don't understand")
            return

        command = msg['text'].strip().lower()

        # Tells who has sent you how many messages
        if command == '/news':
            results = getLastItems()

            self.sender.sendMessage('\n'.join(results))

        # read next sender's messages
        elif command == '/next':
            self.sender.sendMessage("Next!!!!!")

        else:
            self.sender.sendMessage("I don't understand")


class MessageSaver(telepot.helper.Monitor):
    def __init__(self, seed_tuple, store, exclude):
        # The `capture` criteria means to capture all messages.
        super(MessageSaver, self).__init__(seed_tuple, capture=[[lambda msg: not telepot.is_event(msg)]])
        self._store = store
        self._exclude = exclude

    # Store every message, except those whose sender is in the exclude list, or non-text messages.
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if chat_id in self._exclude:
            print('Chat id %d is excluded.' % chat_id)
            return

        if content_type != 'text':
            print('Content type %s is ignored.' % content_type)
            return

        print('Storing message: %s' % msg)
        self._store.put(msg)

import threading

class CustomThread(threading.Thread):
    def start(self):
        print('CustomThread starting ...')
        super(CustomThread, self).start()

# Note how this function wraps around the `call()` function below to implement
# a custom thread for delegation.
def custom_thread(func):
    def f(seed_tuple):
        target = func(seed_tuple)

        if type(target) is tuple:
            run, args, kwargs = target
            t = CustomThread(target=run, args=args, kwargs=kwargs)
        else:
            t = CustomThread(target=target)

        return t
    return f

class ChatBox(telepot.DelegatorBot):
    def __init__(self, token, owner_id):
        self._owner_id = owner_id
        self._seen = set()
        self._store = MongoStore()

        super(ChatBox, self).__init__(token, [
            # Here is a delegate to specially handle owner commands.
            pave_event_space()(
                per_chat_id_in([owner_id]), create_open, CommandsHandler, self._store, timeout=100),

            # Only one MessageSaver is ever spawned for entire application.
            (per_application(), create_open(MessageSaver, self._store, exclude = [])),

            # For senders never seen before, send him a welcome message.
            (self._is_newcomer, call(self._send_welcome)),
        ])

    # seed-calculating function: use returned value to indicate whether to spawn a delegate
    def _is_newcomer(self, msg):
        if telepot.is_event(msg):
            return None

        chat_id = msg['chat']['id']
        if chat_id == self._owner_id:  # Sender is owner
            return None  # No delegate spawned

        if chat_id in self._seen:  # Sender has been seen before
            return None  # No delegate spawned

        self._seen.add(chat_id)
        return []  # non-hashable ==> delegates are independent, no seed association is made.

    async def _send_welcome(self, seed_tuple):
        chat_id = seed_tuple[1]['chat']['id']

        print('Sending welcome ...')
        await self.sendMessage(chat_id, 'Hello!')


TOKEN = "650006953:AAHp3VTA6sGuYFQhvljN7ekZgZ59N4vZBzY"
OWNER_ID = int(154420266)

bot = ChatBox(TOKEN, OWNER_ID)
#loop = asyncio.get_event_loop()
#
#loop.create_task(MessageLoop(bot).run_forever())
#print('Listening ...')

#loop.run_forever()
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)