# bot.py
import os
import time
import math
import json
import asyncio

import discord
from discord.ext.commands import Bot

bot = Bot(command_prefix='~')
#client = discord.Client()

import ggr_utilities
import ggr_emotes

from dotenv import load_dotenv
load_dotenv()



TOKEN = os.getenv("DISCORD_TOKEN")
startup_extensions = ["test", "army"]


@bot.event
async def on_ready():
    global timeReady
    timeReady = time.time()
    
    print('Logged in as {bot.user}')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


timeReady = 0

    





if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(TOKEN)
