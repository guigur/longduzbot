from distutils.command.sdist import sdist
import discord
import os
import certif
from discord.ext import commands
import json
from collections import namedtuple 
import datetime
from dateutil.relativedelta import relativedelta

import sqlite3, os
import ggr_utilities, ggr_emotes
import Com, Database

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

moneyName = lambda a=2: "WAD" if (a >= -1 and a <= 1) else "WADs"
moneyGain = lambda a: "a gagné" if (a >= 0) else "a perdu"
moneyGainEn = lambda a: "won" if (a >= 0) else "lost"

def get_all_users( json_str = False ):
	conn = sqlite3.connect( os.getenv("DATABASE_NAME") )
	conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
	db = conn.cursor()

	rows = db.execute("SELECT * from maitre")

	conn.commit()
	res = rows.fetchall()

	if json_str:
		return json.dumps( [dict(ix) for ix in res] ) #CREATE JSON

	return res

class Eco(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database cog", self,)
		
	######################## DISCORD COMMANDS ########################
			
	def genSalopeiresArrayYear(self, user, guild):
		monthsSaloperies = []
		month = 1
		for month in range(1, 11):
			start_month = datetime.datetime(2023, month, 1)
			end_month = datetime.datetime(2023, month, 1)	+ relativedelta(months=+1)
			monthsSaloperies.append({"month": month, "saloperies": self.database.getStatsSaloperiesMegaarmyOnPeriod(user, guild, start_month.timestamp(), end_month.timestamp())[0]})
		print(monthsSaloperies)
		
		
	@commands.command()
	async def testwad(self, ctx):
		print(get_all_users( True ))

		guild = self.bot.get_guild(806284513583169596)
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""

		self.genSalopeiresArrayYear(ctx.author, guild)
		statsSaloperiesMegaarmyOnPeriod = self.database.getStatsSaloperiesMegaarmyOnPeriod(ctx.author, guild)
		await ctx.send("getStatsSaloperiesMegaarmyOnPeriod " + str(statsSaloperiesMegaarmyOnPeriod))

		statsSaloperieArmyOnPeriod = self.database.getStatsSaloperieArmyOnPeriod(ctx.author, guild)
		await ctx.send("getStatsSaloperieArmyOnPeriod " + str(statsSaloperieArmyOnPeriod))

		statsWadsOnPeriod = self.database.getStatsWadsOnPeriod(ctx.author, guild)
		await ctx.send("getStatsWadsOnPeriod " + str(statsWadsOnPeriod))

		statsWadsBestDayOnPeriod = self.database.getStatsWadsBestDayOnPeriod(ctx.author, guild)
		await ctx.send("getStatsWadsBestDayOnPeriod " + str(statsWadsBestDayOnPeriod))

		statsBestMegaarmyOnPeriod = self.database.getBestMegaarmyOnPeriod(ctx.author, guild)
		await ctx.send("getBestMegaarmyOnPeriod " + str(statsBestMegaarmyOnPeriod))

		statsWorstMegaarmyOnPeriod = self.database.getWorstMegaarmyOnPeriod(ctx.author, guild)
		await ctx.send("getWorstMegaarmyOnPeriod " + str(statsWorstMegaarmyOnPeriod))

		statsBestArmyOnPeriod = self.database.getBestArmyOnPeriod(ctx.author, guild)
		await ctx.send("getBestArmyOnPeriod " + str(statsBestArmyOnPeriod))

		statsWorstArmyOnPeriod = self.database.getWorstArmyOnPeriod(ctx.author, guild)
		await ctx.send("getWorstArmyOnPeriod " + str(statsWorstArmyOnPeriod))


	@commands.command()
	async def wad(self, ctx, arg = None):  #TODO FIX other user
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		if arg:
			try:
				user = await commands.UserConverter().convert(ctx, str(arg))
				await ctx.message.delete()

			except commands.BadArgument:
				await ctx.send("Utilisateur non trouvé")
				ggr_utilities.logger("User not found", self, ctx, ggr_utilities.LogType.ERROR)
				return #on quitte la fonction
		else:
			user = ctx.author
		money = self.database.getDBMoneyVerif(user, ctx.guild)
		userS = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), money[5])
		card = certif.generateMoneyCard(userS, ggr_utilities.serverIcon(ctx.guild))
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def topwad(self, ctx):
		#ggr_utilities.logger(ctx.message.content, self, ctx)
		users = self.findUserMaxBalanceRoutine(ctx.guild)
		if (users != None and len(users) == 3):
		
			try:
				u1 = await self.bot.fetch_user(users[0][1])
				u2 = await self.bot.fetch_user(users[1][1])
				u3 = await self.bot.fetch_user(users[2][1])

				userStruct1 = userStruct(u1.name, u1.discriminator, ggr_utilities.userIcon(u1), users[0][5])
				userStruct2 = userStruct(u2.name, u2.discriminator, ggr_utilities.userIcon(u2), users[1][5])
				userStruct3 = userStruct(u3.name, u3.discriminator, ggr_utilities.userIcon(u3), users[2][5])

				card = certif.generateMoneyPodium(userStruct1, userStruct2, userStruct3, ggr_utilities.serverIcon(ctx.guild), ctx.guild.name)

				await ctx.send(file = discord.File('tmp/card_podium_filled.png'))
			except:
				ggr_utilities.logger("Error generating the topwad card", self, ctx, ggr_utilities.LogType.ERROR)
				await ctx.send("Erreur lors dee la creation la card")
		else:
			ggr_utilities.logger("Not enought members in the money database", self, ctx, ggr_utilities.LogType.INFO)
			await ctx.send("Il n'y a pas assez d'actionnaires du WAD dans la banque !")

	######################### SHELL COMMANDS #########################

	
	############################ ROUTINES ############################

	def findUserMaxBalanceRoutine(self, guild):
		ggr_utilities.logger("Find max balance.", self)
		rows = self.database.getDBMoneyRichOrder(guild, 3)
		return rows
def setup(bot):
	bot.add_cog(Eco(bot))
