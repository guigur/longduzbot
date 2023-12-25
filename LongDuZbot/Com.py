import os
import time
import math
import json
import git
import asyncio
import threading
import signal
from termcolor import colored
from enum import Enum

from pyfiglet import Figlet #shelAscii

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import ggr_utilities
import ggr_emotes
import cmd, sys
from functools import wraps # This convenience func preserves name and docstring


class ObjectComType(Enum):
	NONE = 0
	CHANNEL = 1
	USER = 2

def add_method(cls):
    def decorator(func):
        @wraps(func) 
        def wrapper(self, *args, **kwargs): 
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator

workingId = 0
workingType = ObjectComType.NONE

class Shell(cmd.Cmd):
	def __init__(self, bot):
		cmd.Cmd.__init__(self)
		self.bot = bot
		self.prompt = colored("> ", "light_magenta")
		self.defaultprompt = self.prompt
		self.workingType = ObjectComType.NONE

		self.scheduler = self.bot.get_cog('Scheduler')
		if self.scheduler is None:
			ggr_utilities.logger("Missing Scheduler cog", self, None, ggr_utilities.LogType.ERROR)
	
	f = Figlet(font='slant')
	intro = f.renderText("LongDuZbot") + "\nType help or ? to list commands.\n"
	file = None
	loop = asyncio.get_event_loop()
	
	def stop_server(self):
		ggr_utilities.logger("Stopping server", self, None, ggr_utilities.LogType.INFO)
		#self.scheduler.stop() #does not work
		asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)

	async def get_user(self, id: int):
		self.user = await self.bot.fetch_user(id)
		self.prompt = colored(self.user, "red") + "> "

	async def get_channel(self, id: int):
		self.channel = await self.bot.fetch_channel(id)
		self.prompt  = colored(self.channel.guild.name, "blue") + ">" + colored(self.channel.name, "green") + "> "

	async def user_say(self, id: int, str: str) :
		user = await self.bot.fetch_user(id)
		await user.send(str)

	def do_stop(self, arg):
		'Stop the server'
		self.stop_server()
		return True
        
	def do_EOF(self, line):
		self.stop_server()
		return True

	def do_restart(self, arg):
		'Restart the server'
		ggr_utilities.logger("Restarting server", self)
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

	def do_selectUser(self, arg):
		'select working user'
		if (ggr_utilities.checkIfIdValid(arg)):
			self.user = asyncio.run_coroutine_threadsafe(self.get_user(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.USER

	def do_selectChannel(self, arg):
		'select working chanel'
		if (ggr_utilities.checkIfIdValid(arg)):
			self.channel = asyncio.run_coroutine_threadsafe(self.get_channel(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.CHANNEL

	def do_unselect(self, arg):
		'unseelect user or channel'
		self.user = 0
		self.prompt = self.defaultprompt
		self.channel = 0
		self.workingId = 0
		self.workingType = ObjectComType.NONE

	def do_say(self, arg):
		'say something to the server or chat with an user'
		if (self.workingType != ObjectComType.NONE):
			if (self.workingType == ObjectComType.USER):
				asyncio.run_coroutine_threadsafe(self.user_say(self.workingId, arg), self.loop)
			elif (self.workingType == ObjectComType.CHANNEL):
				workingObject = self.bot.get_channel(self.workingId)
				asyncio.run_coroutine_threadsafe(workingObject.send(arg), self.loop)
		else:
			ggr_utilities.logger("No working ID. Attach a Channel or User with \"selectChannel\" or \"selectUser\"", self, None, ggr_utilities.LogType.ERROR)

class Com(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		x = threading.Thread(target=self.shell_start)
		x.start()

	def shell_start(self):
		self.s = Shell(self.bot)
		self.s.cmdloop()

def setup(bot):
	bot.add_cog(Com(bot))