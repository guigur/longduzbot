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

class ObjectComType(Enum):
	NONE = 0
	CHANNEL = 1
	USER = 2

class Shell(cmd.Cmd):
	def __init__(self, bot):
		cmd.Cmd.__init__(self)
		self.bot = bot

	f = Figlet(font='slant')
	intro = f.renderText("LongDuZbot") + "\nType help or ? to list commands.\n"
	prompt = '> '
	file = None
	loop = asyncio.get_event_loop()
	workingId = 0
	workingType = ObjectComType.NONE
	
	@classmethod
	def changePormpt(self, newPrompt):
		self.prompt = newPrompt

	def stop_server(self):
		ggr_utilities.logger(None, "Stopping server")
		asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
	
	async def get_user(self, id: int):
		user = await self.bot.fetch_user(id)
		self.changePormpt(colored(user, 'red') + " > ")

	async def get_channel(self, id: int):
		channel = await self.bot.fetch_channel(id)
		self.changePormpt(colored(channel.guild.name, 'blue') + " > " + colored(channel.name, 'green') + " > ")

	async def user_say(self, id: int, str: str) :
		user = await self.bot.fetch_user(id)
		await user.send(str)

	def do_version(self, arg):
		'Return the verion hash number'
		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		ggr_utilities.logger(None, "Git version: " + colored(sha, 'blue'))

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
			user = asyncio.run_coroutine_threadsafe(self.get_user(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.USER

	def do_selectChannel(self, arg):
		'select working chanel'
		if (ggr_utilities.checkIfIdValid(int(arg))):
			channel = asyncio.run_coroutine_threadsafe(self.get_channel(int(arg)), self.loop) #check this
			self.workingId = int(arg)
			self.workingType = ObjectComType.CHANNEL

	def do_say(self, arg):
		'say something to the server or chat with an user'
		if (self.workingType != ObjectComType.NONE):
			if (self.workingType == ObjectComType.USER):
				asyncio.run_coroutine_threadsafe(self.user_say(self.workingId, arg), self.loop)
			elif (self.workingType == ObjectComType.CHANNEL):
				workingObject = self.bot.get_channel(self.workingId)
				asyncio.run_coroutine_threadsafe(workingObject.send(arg), self.loop)
		else:
			print("No working ID. Attach a Channel or User with \"selectChannel\" or \"selectUser\"")

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