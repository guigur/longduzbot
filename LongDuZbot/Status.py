import discord
from discord.ext import commands
import sys
import os
import ggr_utilities
import ggr_emotes
import eco

class Status(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# def army():


def setup(bot):
	bot.add_cog(Status(bot))
