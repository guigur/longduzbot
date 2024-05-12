import discord
from discord.ext import commands
import sys
import os

import ggr_utilities, ggr_emotes
import Eco, Com

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	


	######################## DISCORD COMMANDS ########################
	
	# @commands.command()
	# async def testeEmbed(self, ctx):
	# 	embed=discord.Embed(color=0xFF5733)
	# 	embed.add_field(name="undefined", value="undefined", inline=False)
	# 	await ctx.send(embed=embed)

	# @commands.command()
	# async def foo(self, ctx, arg = None):
	# 	if arg:
	# 		try:
	# 			user = await commands.UserConverter().convert(ctx, str(arg))
	# 			await ctx.send("arg " + user.name)
	# 		except commands.BadArgument:
	# 			await ctx.send("Utilisateur non trouvé")

	# 	else:
	# 		await ctx.send("no arg " + ctx.author.name)

	######################### SHELL COMMANDS #########################

	############################ ROUTINES ############################

def setup(bot):
	bot.add_cog(Test(bot))

def teardown(bot):
	print('test I am being unloaded!')

		#os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
		#print("exit")
		#sys.exit(0)
		#await ctx.send("test")
		#await ctx.send(ctx.author.name)
	
		#eco.Eco.changeBallance(ctx.author, 20)
