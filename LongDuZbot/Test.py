import discord
from discord.ext import commands
import sys
import os
import sqlite3
import time

import ggr_utilities, ggr_emotes
import Eco, Com

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect("test.db")
		cursor = self.connection.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY, command TEXT, timestamp INTEGER)")
		cursor.execute("INSERT INTO commands(command, timestamp) VALUES(?,?)", ('test', str(int(time.time()))))



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

async def setup(bot):
	await bot.add_cog(Test(bot))

def teardown(bot):
	print('I am being unloaded!')

		#os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
		#print("exit")
		#sys.exit(0)
		#await ctx.send("test")
		#await ctx.send(ctx.author.name)
	
		#eco.Eco.changeBallance(ctx.author, 20)
