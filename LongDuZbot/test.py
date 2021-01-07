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
		await ctx.send("test")
		await ctx.send(ctx.author.name)
	
		#eco.Eco.changeBallance(ctx.author, 20)
def setup(bot):
	bot.add_cog(Test(bot))
