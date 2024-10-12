import discord
from discord.ext import commands
import sys
import os
import ggr_utilities, ggr_emotes
import Eco

class Status(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " cog Unloaded!" , self, None, ggr_utilities.LogType.WARN)

######################## DISCORD COMMANDS ########################

######################### SHELL COMMANDS #########################

############################ ROUTINES ############################

def setup(bot):
	bot.add_cog(Status(bot))
