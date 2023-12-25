import os
import time
import math
import json
import git
import asyncio
import threading
import signal
import schedule
import time
from termcolor import colored
from enum import Enum


import discord
from discord.ext import commands
from discord.ext.commands import Bot

import ggr_utilities
import ggr_emotes

import sys
from functools import wraps # This convenience func preserves name and docstring


# class Events():
# 	def __init__(self, bot):
# 		self.bot = bot

class Scheduler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.isRunning = True
		
		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database cog", self, ggr_utilities.LogType.ERROR)

		schedule.every().day.at("01:02").do(self.job)

		x = threading.Thread(target=self.loop)
		x.start()

	def job(self):
		asyncio.run(self.stuff())

		#guild = self.bot.fetch_guild(495361629806919691)
		#print(guild.name)
		#self.database.changeDBBalanceMoney(user, guild, 100)
		print("I'm working...")
		print(time.time())

	async def stuff(self):
		user = await self.bot.fetch_user(789670200294899713)
		#print(guild.name)
		print(user)

	def loop(self):
		while self.isRunning:
			schedule.run_pending()
			time.sleep(1)

	def stop(self):
		self.isRunning = False
		ggr_utilities.logger("Stopping the scheduler", self, None, ggr_utilities.LogType.INFO)

def setup(bot):
	bot.add_cog(Scheduler(bot))