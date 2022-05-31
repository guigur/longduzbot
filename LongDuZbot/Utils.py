import discord
from discord.ext import commands
import ggr_utilities
import git
from termcolor import colored
import Com

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	######################## DISCORD COMMANDS ########################

	@commands.command()
	async def version(self, ctx):
		"""Affiche la version du bot."""
		ggr_utilities.logger(ctx, ctx.message.content)
		await ctx.send("Git version: **" + self.verisonRoutine() + "**")

	######################### SHELL COMMANDS #########################

	@Com.add_method(Com.Shell)
	def do_version(arg):
		'Return the verion hash number'
		ggr_utilities.logger(None, "Git version: " + colored(Utils.verisonRoutine(), 'blue'))
	
	############################ ROUTINES ############################
	
	@classmethod
	def verisonRoutine(self):
		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		return(sha)

def setup(bot):
	bot.add_cog(Utils(bot))