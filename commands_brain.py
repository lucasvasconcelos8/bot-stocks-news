from commands_services import CommandsServices
from util import handleArgs
import telepot

#Class for handle Commands and Messages Actions
class CommandsBrain(telepot.helper.ChatHandler):
	def __init__(self, seed_tuple, store, **kwargs):
		super(CommandsBrain, self).__init__(seed_tuple, **kwargs)
		self._store = store
		self._services = CommandsServices()

	#CENTRAL FUNCTION TO ANSWER A MESSAGE SENT FOR AN USER.
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		if content_type != 'text':
			self.sender.sendMessage("I don't understand")
			return

		command = msg['text'].lower().split(' ')[0]

		args = handleArgs(msg['text'].lower())

		self.identify_command(command, args)

	#Function to define each command and action to do.
	def identify_command(self, command, args):

		# Tells who has sent you how many messages
		if command == '/news':
			if args == "" :
				results = self._store.getLastItems(int(0))
			else:
				results = self._store.getLastItems(int(args[0]))

			self.sender.sendMessage('\n'.join(results))

		elif command == '/stock':
			if args == "":
				self.sender.sendMessage("I need more info men")
			else:
				results = self._services.analysis_stock(str(args[0]), float(args[1]), float(args[2]), float(args[3]))
				print(results)
				self.sender.sendMessage(results, parse_mode="Markdown")

		# read next sender's messages
		elif command == '/next':
			self.sender.sendMessage("Next!!!!!")
		elif command == '/help':
			text = str(self._services.help_commands())
			print(text)
			self.sender.sendMessage(text, parse_mode="Markdown")

		else:
			self.sender.sendMessage("I don't understand")