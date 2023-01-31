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

token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("DISCORD_COMMAND_PREFIX")

#Com need to loaded first. Otherwise, the additional commands in other modules wont be utilized
startup_extensions = ["Com", "Utils", "Eco", "Army", "Test", "Admin"] #"status",

intents = discord.Intents.all()
intents.members = True

bot = Bot(command_prefix=prefix, intents=intents)

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
	bot.run(token)
