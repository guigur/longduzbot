import discord
from discord.ext import commands
import ggr_utilities
import git

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def version(self, ctx):
		"""Affiche la version du bot."""
		ggr_utilities.logger(ctx, ctx.message.content)

		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		await ctx.send("Git version: " + sha)

def setup(bot):
	bot.add_cog(Utils(bot))