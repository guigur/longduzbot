import discord
from discord.ext import commands
import sys
import os
import ggr_utilities, ggr_emotes
import Eco

class Status(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

######################## DISCORD COMMANDS ########################

######################### SHELL COMMANDS #########################

############################ ROUTINES ############################

async def setup(bot):
	await bot.add_cog(Status(bot))
