#Functions to help clean and organize the code.


#function for define args empty or not
def handleArgs(string_args):
	list_args = string_args.split(' ')
	if len(list_args) > 1:
		return list_args[1:]
	else:
		""