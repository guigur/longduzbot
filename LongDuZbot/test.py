import discord
from discord.ext import commands
import ggr_utilities
import ggr_emotes
import eco

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx):
		"""Test"""
		eco.Eco.changeBallance(self, ctx.author, 20)
def setup(bot):
	bot.add_cog(Test(bot))
