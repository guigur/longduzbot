# bot.py
import os
import time
import math
import json
import asyncio

import discord
from discord.ext.commands import Bot

import ggr_utilities
import ggr_emotes

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
startup_extensions = ["test", "army", "ulian", "teub"]

bot = Bot(command_prefix='~')

@bot.event
async def on_ready():
	global timeReady
	timeReady = time.time()
	ggr_utilities.logger(None, "Logged in as " + bot.user.name + " " + str(bot.user.id))

timeReady = 0

if __name__ == "__main__":
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			ggr_utilities.logger(None, "Loaded extension " + extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			ggr_utilities.logger(None, "Failed to load extension " + extension + " \n" + exc)
	bot.run(TOKEN)
