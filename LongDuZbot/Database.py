import discord
from discord.ext import commands
import sys
import os
import sqlite3
import json
import time
from enum import Enum

import ggr_utilities, ggr_emotes
import Eco, Com

class MaitreJeanfoutreType(Enum):
	MAITRE = 0
	JEANFOUTRE = 1

	def data(self):
		if (self.value == 0):
			return ({ "table":"maitre", "idkey":"maitreID"})
		elif (self.value == 1):
			return ({ "table":"jeanfoutre", "idkey":"jeanfoutreID"})


class Database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = "test.db"
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()
		self.requestDB("CREATE TABLE army (armyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, saloperies, wad)")
		self.requestDB("CREATE TABLE megaarmy (megaarmyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, lines, saloperies, wad)")
		self.requestDB("CREATE TABLE maitre (maitreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
		self.requestDB("CREATE TABLE jeanfoutre (jeanfoutreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
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

	@commands.command()
	async def foo(self, ctx, arg = None):
		self.setDBMaitre(1, "test", 1, "guild", time.time(), 10, 1)

	@commands.command()
	async def hardreset(self, ctx, arg = None):
		"""Hard reset the Maitre and Jeanfoutre"""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		await ggr_utilities.sudemote(ctx)
		self.setDBArchiveMaitreJeanfoutre(MaitreJeanfoutreType.MAITRE)

	############################ ROUTINES ############################

	def setDBMaitreJeanfoutre(self, type, userID, user, guildID, guild, timestamp, saloperies, megaarmyID):
		tableID = "NULL"
		request = "SELECT " + type.data()['idkey'] + ", isArchive FROM " + type.data()['table'] + " ORDER BY " + type.data()['idkey'] + " DESC LIMIT 1"
		self.requestDB(request)
		row = self.cur.fetchone()
		if (row is None or row[1] != 0):
			ggr_utilities.logger("No pass " + type.data()['table'] + " using a new line", self)
		else:
			ggr_utilities.logger("Old " + type.data()['table'] + " is out, using his old line " + str(row[0]), self)
			tableID = str(row[0])
		
		request = "REPLACE INTO " + type.data()['table'] + " VALUES(" + tableID + ", " + str(int(userID)) + ", " + self.escape(user) + ", " + \
		str(int(guildID)) + ", " + self.escape(guild) + ", " + str(float(timestamp)) + ", " + \
		str(int(saloperies)) + ", " + str(int(megaarmyID)) + ", " + str(0) + ")"
		ggr_utilities.logger("Request:  " + request, self)
		self.requestDB(request)
		return(self.cur.lastrowid)
	
	def getDBMaitreJeanfoutre(self, type):
		request = "SELECT * FROM " + type.data()['table'] + " WHERE isArchive=0 ORDER BY " + type.data()['idkey'] + " DESC LIMIT 1"
		self.requestDB(request)
		row = self.cur.fetchone()
		return (row)

	def setDBArchiveMaitreJeanfoutre(self, type):
		request = "UPDATE " + type.data()['table'] + " SET isArchive = 1 WHERE isArchive = 0"
		self.requestDB(request)

	####
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
			ggr_utilities.logger(str(e), self)
		else:
			ggr_utilities.logger("Request OK", self)

def setup(bot):
	bot.add_cog(Database(bot))

def teardown(bot):
	print('I am being unloaded!')
