import discord
from discord.ext import commands
import ggr_utilities
import git
from termcolor import colored
import Com

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@Com.add_method(Com.Shell)
	def do_version(arg):
		'Return the verion hash number'
		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		ggr_utilities.logger(None, "Git version: " + colored(sha, 'blue'))

	@commands.command()
	async def version(self, ctx):
		"""Affiche la version du bot."""
		ggr_utilities.logger(ctx, ctx.message.content)

		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		await ctx.send("Git version: " + sha)

def setup(bot):
	bot.add_cog(Utils(bot))