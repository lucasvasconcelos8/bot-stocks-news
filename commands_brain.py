from commands_services import CommandsServices

#Class for handle MongoAccess
class CommandsBrain(object):
	def __init__(self):
		self.message = ''
		self._services = CommandsServices()

	def identify_command(self, command):

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