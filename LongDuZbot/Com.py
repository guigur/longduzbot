import discord
from discord.ext import commands
import sys
import threading
import time
import cmd
from enum import Enum
from pyfiglet import Figlet #shelAscii
import asyncio
import signal

import ggr_utilities
import ggr_emotes

####################################################
def signal_handler(sig, frame):
	print("^C")
	Shell.stop_server()

####################################################

async def get_user(id: int):
	user = await self.bot.fetch_user(id)
	Shell.changePormpt(colored(user, 'red') + " > ")

async def get_channel(id: int):
	channel = await self.bot.fetch_channel(id)
	Shell.changePormpt(colored(channel.guild.name, 'blue') + " > " + colored(channel.name, 'green') + " > ")

async def user_say(id: int, str: str) :
	user = await self.bot.fetch_user(id)
	await user.send(str)

class ObjectComType(Enum):
	NONE = 0
	CHANNEL = 1
	USER = 2

class Shell(cmd.Cmd):
	f = Figlet(font='slant')
	intro = f.renderText("LongDuZbot") + "\nType help or ? to list commands.\n"
	prompt = '> '
	file = None
	#channel = None
	loop = asyncio.get_event_loop()
	workingId = 0
	workingType = ObjectComType.NONE
	
	def init(self, bot):
		self.bot = bot

	@classmethod
	def changePormpt(self, newPrompt):
		self.prompt = newPrompt

	@classmethod
	def stop_server(self):
		ggr_utilities.logger(None, "Stopping server")
		asyncio.run_coroutine_threadsafe(self.bot.logout(), self.loop)

	def do_stop(self, arg):
		'Stop the server'
		self.stop_server()
		return True
    
	def do_EOF(self, line):
		self.stop_server()
		return True

	def do_restart(self, arg):
		'Restart the server'
		ggr_utilities.logger(None, "Restarting server")
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

	def do_selectUser(self, arg):
		'select working user'
		if (ggr_utilities.checkIfIdValid(int(arg))):
			user = asyncio.run_coroutine_threadsafe(get_user(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.USER

	def do_selectChannel(self, arg):
		'select working chanel'
		if (ggr_utilities.checkIfIdValid(int(arg))):
			channel = asyncio.run_coroutine_threadsafe(get_channel(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.CHANNEL

	def do_say(self, arg):
		'say something to the server'
		if (self.workingType != ObjectComType.NONE):
			if (self.workingType == ObjectComType.USER):
				asyncio.run_coroutine_threadsafe(user_say(self.workingId, arg), self.loop)
			elif (self.workingType == ObjectComType.CHANNEL):
				workingObject = self.bot.get_channel(self.workingId)
				asyncio.run_coroutine_threadsafe(workingObject.send(arg), self.loop)
		else:
			print("No working ID. Attach a Channel or User with \"selectChannel\" or \"selectUser\"")

#def checkIfChanExist(self):
#TODO


def start_shell(bot):
	Shell().init(bot)
	Shell().cmdloop()
	

class Com(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		signal.signal(signal.SIGINT, signal_handler)
		x = threading.Thread(target=start_shell(bot))
		x.start()
		
def setup(bot):
	bot.add_cog(Com(bot))
