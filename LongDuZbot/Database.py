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
		self.db = os.getenv("DATABASE_NAME")
		ggr_utilities.logger("Using database: " + self.db , self, None, ggr_utilities.LogType.INFO)
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()

		self.requestDB("CREATE TABLE money (moneyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, money)")
		self.requestDB("CREATE TABLE moneyTransaction (moneyTransactionID INTEGER PRIMARY KEY AUTOINCREMENT, userEmitterID, userEmitter, userReceiverID, userReceiver, guildID, guild, timestamp, money)")

		self.requestDB("CREATE TABLE army (armyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, saloperies, money)")
		self.requestDB("CREATE TABLE megaarmy (megaarmyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, lines, saloperies, money)")

		self.requestDB("CREATE TABLE maitre (maitreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
		self.requestDB("CREATE TABLE jeanfoutre (jeanfoutreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
		
		self.escape = lambda a: json.dumps(a.replace("\"", ""))

	######################## DISCORD COMMANDS ########################
	
	# @commands.command()
	# async def testeEmbed(self, ctx):
	#   embed=discord.Embed(color=0xFF5733)
	#   embed.add_field(name="undefined", value="undefined", inline=False)
	#   await ctx.send(embed=embed)


	######################### SHELL COMMANDS #########################

	############################ ROUTINES ############################

	### ECO
		
	def periodHelper(self, startTimestamp, endTimestamp):
		if (startTimestamp != None and endTimestamp != None):
			return (" AND timestamp > " + str(startTimestamp) + " AND timestamp < " + str(endTimestamp))
		return ""

	def getStatsPercentileSaloperiesMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT * FROM (SELECT userID, guildID, SUM(saloperies) AS total_saloperies, 100 - PERCENT_RANK() OVE (ORDER BY SUM(saloperies) DESC) * 100 AS percentile_rankR FROM megaarmy WHERE guildID=" + str(guild.id) + " GROUP BY userID, guildID) AS subquery WHERE userID =" + str(user.id) + ";"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)
	
	def getStatsPercentileCommandMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT * FROM (SELECT userID, guildID, count(*) AS total_saloperies, 100 - PERCENT_RANK() OVER (ORDER BY COUNT(saloperies) DESC) * 100 AS percentile_rank, * FROM megaarmy WHERE guildID=" + str(guild.id) + " GROUP BY userID, guildID) AS subquery WHERE userID =" + str(user.id) + ";"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getStatsCountSaloperiesMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT COUNT(*) AS nbr_cmds, * FROM megaarmy WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp)
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getStatsBestDaySaloperiesMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT strftime('%Y-%m-%d', timestamp, 'unixepoch') AS day, timestamp, SUM(saloperies) AS max_saloperies FROM megaarmy WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " GROUP BY day ORDER BY max_saloperies DESC LIMIT 1;"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getStatsSaloperiesMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT COALESCE(SUM(saloperies), 0) AS sumSaloperies FROM megaarmy WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1;"
		self.requestDB(request)
		#print(self.cur.description)
		res = self.cur.fetchall()
		#j = json.dumps( [dict(ix) for ix in res] ) #CREATE JSON
		#print(j)
		return (res)

	def getStatsSaloperieArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT COALESCE(SUM(saloperies), 0) FROM army WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()[0]
		return (res)
	
	def getStatsWadsOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT COALESCE(SUM(money), 0) FROM moneyTransaction WHERE userReceiverID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getStatsWadsBestDayOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT *, COALESCE(MAX(money), 0) AS maxMoney FROM moneyTransaction WHERE userReceiverID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getBestMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT *, COALESCE(MAX(saloperies), 0) AS maxSaloperies FROM megaarmy WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getStatsPercentileWads(self, user, guild):
		request = "SELECT * FROM (SELECT userID, guildID, money, 100 - PERCENT_RANK() OVER (ORDER BY money DESC) * 100 AS percentile_rank, * FROM money WHERE guildID=" + str(guild.id) + " GROUP BY userID, guildID) AS subquery WHERE userID =" + str(user.id) + ";"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getWorstMegaarmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT *, COALESCE(MIN(saloperies), 0) AS maxSaloperies FROM megaarmy WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)

	def getBestArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT *, COALESCE(MAX(saloperies), 0) AS maxSaloperies FROM army WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)
	
	def getWorstArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		request = "SELECT *, COALESCE(MIN(saloperies), 0) AS maxSaloperies FROM army WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + self.periodHelper(startTimestamp, endTimestamp) + " LIMIT 1"
		self.requestDB(request)
		res = self.cur.fetchone()
		return (res)
	
	def getDBMoneyRichOrder(self, guild, limit=0):
		filter = ""
		if(limit > 0):
			filter = " DESC LIMIT 3"
		request = "SELECT * FROM money ORDER BY money" + filter
		self.requestDB(request)
		rows = self.cur.fetchall()
		return (rows)

	def getDBMoneyVerif(self, user, guild):
		money = self.getDBMoney(user, guild)
		if (money == None):
			self.createDBAccountMoney(user, guild)
		return (self.getDBMoney(user, guild))
	
	def getDBMoney(self, user, guild):
		request = "SELECT * FROM money WHERE userID=" + str(user.id) +" AND guildID=" + str(guild.id) + " ORDER BY moneyID DESC LIMIT 1"
		self.requestDB(request)
		money = self.cur.fetchone()
		return (money)
	
	def createDBAccountMoney(self, user, guild):
		freeStartingMoney = 1
		if (self.getDBMoney(user, guild) == None):
			request = "REPLACE INTO money VALUES(NULL, " + str(int(user.id)) + ", " + self.escape(user.name) + ", " + \
			str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + str(freeStartingMoney) + ")"
			self.requestDB(request)
			ggr_utilities.logger("Welcome the bank of " + Eco.moneyName() + " " + user.name, self)
		else:
			ggr_utilities.logger("The account for user " + user.name + " already exist", self)

	def changeDBBalanceMoney(self, user, guild, diff):
		currentBalance = self.getDBMoneyVerif(user, guild)

		newMoney = currentBalance[5] + diff
		moneyID = currentBalance[0]

		request = "REPLACE INTO money VALUES(" + str(moneyID) + ", " + str(int(user.id)) + ", " + self.escape(user.name) + ", " + \
		str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + str(newMoney) + ")"
		self.requestDB(request)
		self.logDBMoneyTransaction(guild, user, guild, time.time(), diff)


	def logDBMoneyTransaction(self, userEmitter, userReceiver, guild, timestamp, money):
		request = "INSERT INTO moneyTransaction VALUES(NULL, " + \
		str(int(userEmitter.id)) + ", " + self.escape(userEmitter.name) + ", " + \
		str(int(userReceiver.id)) + ", " + self.escape(userReceiver.name) + ", " + \
		str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + \
		str(timestamp) + ", " + str(money) + ")"
		self.requestDB(request)

	### ARMY
	def setDBMaitreJeanfoutre(self, type, user, guild, timestamp, saloperies, megaarmyID):
		tableID = "NULL"
		request = "SELECT " + type.data()['idkey'] + ", isArchive FROM " + type.data()['table'] + " ORDER BY " + type.data()['idkey'] + " DESC LIMIT 1"
		self.requestDB(request)
		row = self.cur.fetchone()
		if (row is None or row[1] != 0):
			ggr_utilities.logger("No past " + type.data()['table'] + ". Creating a new line!", self)
		else:
			ggr_utilities.logger("Old " + type.data()['table'] + " is out, using his old line " + str(row[0]), self)
			tableID = str(row[0])
		
		request = "REPLACE INTO " + type.data()['table'] + " VALUES(" + tableID + ", " + str(int(user.id)) + ", " + self.escape(user.name) + ", " + \
		str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + str(float(timestamp)) + ", " + \
		str(int(saloperies)) + ", " + str(int(megaarmyID)) + ", " + str(0) + ")"
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

	def addDBArmy(self, user, guild, timestamp, command, saloperies, money):
		request = "INSERT INTO army VALUES(NULL, " + str(int(user.id)) + ", " + self.escape(user.name) + ", " + \
		str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + str(float(timestamp)) + ", " + \
		self.escape(command) + ", " + str(int(saloperies)) + ", " + str(int(money)) + ")"
		self.requestDB(request)
		return(self.cur.lastrowid)

	def addDBMegaArmy(self, user, guild, timestamp, command, lines, saloperies, money):
		request = "INSERT INTO megaarmy VALUES(NULL," + str(int(user.id)) + ", " + self.escape(user.name) + ", " + \
		str(int(guild.id)) + ", " + self.escape(guild.name) + ", " + str(float(timestamp)) + ", " + \
		self.escape(command) + ", " + str(int(lines)) + ", " + str(int(saloperies)) + ", " + str(int(money)) + ")"
		self.requestDB(request)
		return(self.cur.lastrowid)

	### GENERAL
	def requestDB(self, request):
		ggr_utilities.logger("Request:  " + request, self)
		try:
			self.cur.execute(request)
			self.con.commit()
		except sqlite3.OperationalError as e:
			ggr_utilities.logger(str(e), self, None, ggr_utilities.LogType.INFO)
		else:
			ggr_utilities.logger("Request OK", self, None, ggr_utilities.LogType.SUCCESS)

def setup(bot):
	bot.add_cog(Database(bot))

def teardown(bot):
	print('I am being unloaded!')
