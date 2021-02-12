import os
import time
import math
import json
import asyncio
import threading

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


class Com(cmd.Cmd):
	f = Figlet(font='slant')
	intro = f.renderText("LongDuZbot") + "\nType help or ? to list commands.\n"
	prompt = '> '
	file = None

	def do_stop(self, arg):
		'Stop the server'
		ggr_utilities.logger(None, "Stopping server")
		y.stop()
		sys.exit(0)

	def do_restart(self, arg):
		'Restart the server'
		ggr_utilities.logger(None, "Restarting server")
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

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
