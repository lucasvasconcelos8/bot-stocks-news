import markdown
import math

#Class for deliver functions to create data in commands.
class CommandsServices():
	def __init__(self):
		self.test = 'teste'

	#function to show information about commands
	def help_commands(self):
		#return str(markdown.Markdown("help.md"))
		return str(open('help.md', 'r').read())

	#function to calculate buyout minimum and profits for a 
	#	given buyin and buyout price. 
	def analysis_stock(self, name, buy_in, count, buy_out):
		buy_out_minimum = round(((int(buy_in)*count)+5)/count,2)
		profit =  round( ((buy_out*count) - 5) - (buy_in*count) )
		profit_percent = round( (profit / buy_in)*100 )

		return str("*"+str(name)+"*\n\n")+str(" - buy in: R$"+str(buy_in)+"\n")+str(" - buy out minimum: R$"+str(buy_out_minimum)+"\n")+str(" - buy out: R$"+str(buy_out)+"\n")+str(" - profit: R$"+str(profit)+"\n")+str(" - profit percent : "+str(profit_percent)+"%"+"\n")