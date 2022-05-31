import discord
from discord.ext import commands
import ggr_utilities
import sqlite3
import os

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def claim(self, ctx):
		"""Ce serveur de saloperies est a moi."""
		ggr_utilities.logger(ctx, ctx.message.content)
		self.initTable()
		await ctx.send("Git version: ")

	def initTable(self):
		database = os.getenv("DATABASE_NAME")
		con = sqlite3.connect(database)
		cur = con.cursor()
		
		try:
			cur.execute('''CREATE TABLE Admin(userID real, guildID real)''')
		except:
			pass
		#cur.execute("INSERT INTO Admin VALUES ('1', '1')")
		con.commit()
		con.close()

def setup(bot):
	bot.add_cog(Admin(bot))