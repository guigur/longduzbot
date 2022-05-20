import os
import time
import math
import json
import threading

import discord
from discord.ext.commands import Bot

import ggr_utilities
import ggr_emotes

import cmd, sys

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("DISCORD_COMMAND_PREFIX")
startup_extensions = ["Com", "Utils", "eco", "army", "test"] #"status",

bot = Bot(command_prefix=prefix)

@bot.event
async def on_ready():
	global timeReady
	timeReady = time.time()
	ggr_utilities.logger(None, "Logged in as " + bot.user.name + " " + str(bot.user.id))
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='les !megaarmy'))
	
def load_extentions():
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			ggr_utilities.logger(None, "Loaded extension " + extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			ggr_utilities.logger(None, "Failed to load extension " + extension + " \n" + exc)

if __name__ == "__main__":
	load_extentions()
	bot.run(TOKEN)
