import discord
from discord.ext import commands
import sys
import os
import sqlite3
import json

import ggr_utilities, ggr_emotes
import Eco, Com

class Database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = "test.db"
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()
		self.requestDB("CREATE TABLE army (armyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, saloperies, wad)")
		self.requestDB("CREATE TABLE megaarmy (megaarmyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, lines, saloperies, wad)")
		self.requestDB("CREATE TABLE maitre (maitreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
		self.requestDB("CREATE TABLE jeanfoutre (jeanfoutreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies)")
		self.escape = lambda a: json.dumps(a.replace("\"", ""))

	######################## DISCORD COMMANDS ########################
	
	# @commands.command()
	# async def testeEmbed(self, ctx):
	#   embed=discord.Embed(color=0xFF5733)
	#   embed.add_field(name="undefined", value="undefined", inline=False)
	#   await ctx.send(embed=embed)

	# @commands.command()
	# async def foo(self, ctx, arg = None):
	#   if arg:
	#       try:
	#           user = await commands.UserConverter().convert(ctx, str(arg))
	#           await ctx.send("arg " + user.name)
	#       except commands.BadArgument:
	#           await ctx.send("Utilisateur non trouvé")

	#   else:
	#       await ctx.send("no arg " + ctx.author.name)

	######################### SHELL COMMANDS #########################

	############################ ROUTINES ############################

	def setDBMaitre(self, userID, user, guildID, guild, timestamp, saloperies, megaarmyID):
		request = "INSERT INTO maitre VALUES(NULL," + str(int(userID)) + ", " + self.escape(user) + ", " + \
		str(int(guildID)) + ", " + self.escape(guild) + ", " + str(float(timestamp)) + ", " + \
		str(int(saloperies)) + ", " + str(int(megaarmyID)) + ")"
		ggr_utilities.logger("Request:  " + request, self)
		self.requestDB(request)
		return(self.cur.lastrowid)


	def addDBArmy(self, userID, user, guildID, guild, timestamp, command, saloperies, wad):
		request = "INSERT INTO army VALUES(NULL, " + str(int(userID)) + ", " + self.escape(user) + ", " + \
		str(int(guildID)) + ", " + self.escape(guild) + ", " + str(float(timestamp)) + ", " + \
		self.escape(command) + ", " + str(int(saloperies)) + ", " + str(int(wad)) + ")"
		ggr_utilities.logger("Request:  " + request, self)
		self.requestDB(request)
		return(self.cur.lastrowid)


	def addDBMegaArmy(self, userID, user, guildID, guild, timestamp, command, lines, saloperies, wad):
		request = "INSERT INTO megaarmy VALUES(NULL," + str(int(userID)) + ", " + self.escape(user) + ", " + \
		str(int(guildID)) + ", " + self.escape(guild) + ", " + str(float(timestamp)) + ", " + \
		self.escape(command) + ", " + str(int(lines)) + ", " + str(int(saloperies)) + ", " + str(int(wad)) + ")"
		ggr_utilities.logger("Request:  " + request, self)
		self.requestDB(request)
		return(self.cur.lastrowid)

	def requestDB(self, request):
		try:
			self.cur.execute(request)
			self.con.commit()
		except sqlite3.OperationalError as e:
			if (request.__contains__("CREATE")):
				ggr_utilities.logger(str(e) + " > Table '" + self.getTablename(request, " ") + "' already exist", self)
			else:
				ggr_utilities.logger(str(e), self)
		else:
			ggr_utilities.logger("Request OK", self)

	def getTablename(self, request, breakword):
		res = request.split(breakword)
		return (res[2])

def setup(bot):
	bot.add_cog(Database(bot))

def teardown(bot):
	print('I am being unloaded!')

