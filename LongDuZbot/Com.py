import discord
from discord.ext import commands
import sys
import threading
import time
import cmd

import ggr_utilities
import ggr_emotes


class Com(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


def setup(bot):
	bot.add_cog(Com(bot))
