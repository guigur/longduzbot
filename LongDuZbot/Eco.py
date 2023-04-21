from distutils.command.sdist import sdist
import discord
import os
import certif
from discord.ext import commands
import json
from collections import namedtuple 

import ggr_utilities, ggr_emotes
import Com, Database

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

moneyName = lambda a=2: "WAD" if (a >= -1 and a <= 1) else "WADs"
moneyGain = lambda a: "a gagné" if (a >= 0) else "a perdu"
moneyGainEn = lambda a: "won" if (a >= 0) else "lost"

class Eco(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database cog", self,)
		
	######################## DISCORD COMMANDS ########################

	@commands.command()
	async def wad(self, ctx, arg = None):  #TODO FIX other user
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		if arg:
			try:
				user = await commands.UserConverter().convert(ctx, str(arg))
			except commands.BadArgument:
				await ctx.send("Utilisateur non trouvé")
				ggr_utilities.logger(ctx, "User not found")
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
