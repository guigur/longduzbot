import os
import time
import math
import json
import asyncio
import threading
from termcolor import colored
from enum import Enum

from pyfiglet import Figlet #shelAscii

import discord
from discord.ext.commands import Bot

import ggr_utilities
import ggr_emotes

import cmd, sys

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("DISCORD_COMMAND_PREFIX")
startup_extensions = ["com",  "army", "ulian", "teub", "eco", "test"]

bot = Bot(command_prefix=prefix)

@bot.event
async def on_ready():
	global timeReady
	timeReady = time.time()
	ggr_utilities.logger(None, "Logged in as " + bot.user.name + " " + str(bot.user.id))

def bot_start():
	bot.run(TOKEN)

def shell_start():
	Com().cmdloop()
y = threading.Thread(target=bot_start)

####################################################

async def get_user(id: int):
	user = await bot.fetch_user(id)
	Com.changePormpt(colored(user, 'red') + " > ")

async def get_channel(id: int):
	channel = await bot.fetch_channel(id)
	Com.changePormpt(colored(channel.guild.name, 'blue') + " > " + colored(channel.name, 'green') + " > ")

async def user_say(id: int, str: str) :
	user = await bot.fetch_user(id)
	await user.send(str)

class ObjectComType(Enum):
	NONE = 0
	CHANNEL = 1
	USER = 2

class Com(cmd.Cmd):
	f = Figlet(font='slant')
	intro = f.renderText("LongDuZbot") + "\nType help or ? to list commands.\n"
	prompt = '> '
	file = None
	#channel = None
	loop = asyncio.get_event_loop()
	workingId = 0
	workingType = ObjectComType.NONE
	
	@classmethod
	def changePormpt(self, newPrompt):
		self.prompt = newPrompt

	def do_stop(self, arg):
		'Stop the server'
		ggr_utilities.logger(None, "Stopping server")
		#y.stop()
		#TODO: kill all threads
		sys.exit(0)

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
				workingObject = bot.get_channel(self.workingId)
				asyncio.run_coroutine_threadsafe(workingObject.send(arg), self.loop)
		else:
			print("No working ID. Attach a Channel or User with \"selectChannel\" or \"selectUser\"")


def checkIfChanExist(self):
	#TODO
	print("S")

def parse(arg):
	'Convert a series of zero or more numbers to an argument tuple'
	return tuple(map(int, arg.split()))

if __name__ == "__main__":
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			ggr_utilities.logger(None, "Loaded extension " + extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			ggr_utilities.logger(None, "Failed to load extension " + extension + " \n" + exc)
	


#x = threading.Thread(target=shell_start)

#x.start()
y.start()
shell_start()