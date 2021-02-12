import discord
from discord.ext import commands
import sys
import os
import ggr_utilities
import ggr_emotes
import eco

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx):
		"""Test"""
		print("restart")
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
		#print("exit")
		#sys.exit(0)
		#await ctx.send("test")
		#await ctx.send(ctx.author.name)
	
		#eco.Eco.changeBallance(ctx.author, 20)
def setup(bot):
	bot.add_cog(Test(bot))
