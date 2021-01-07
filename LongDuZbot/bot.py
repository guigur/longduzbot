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
prefix = os.getenv("DISCORD_COMMAND_PREFIX")
startup_extensions = ["com",  "army", "ulian", "teub", "eco", "test"]

bot = Bot(command_prefix=prefix)

@bot.event
async def on_ready():
	global timeReady
	timeReady = time.time()
	ggr_utilities.logger(None, "Logged in as " + bot.user.name + " " + str(bot.user.id))


if __name__ == "__main__":
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			ggr_utilities.logger(None, "Loaded extension " + extension)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			ggr_utilities.logger(None, "Failed to load extension " + extension + " \n" + exc)


bot.run(TOKEN)
