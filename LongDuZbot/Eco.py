from distutils.command.sdist import sdist
import discord
import os
import certif
from discord.ext import commands
import json
from collections import namedtuple 

import ggr_utilities, ggr_emotes
import Com

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

class Eco(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	######################## DISCORD COMMANDS ########################

	@commands.command()
	async def wad(self, ctx, arg = None):
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""
		ggr_utilities.logger(ctx, ctx.message.content)
		if arg:
			try:
				user = await commands.UserConverter().convert(ctx, str(arg))
			except commands.BadArgument:
				await ctx.send("Utilisateur non trouvé")
				ggr_utilities.logger(ctx, "User not found")
				return #on quitte la fonction
		else:
			user = ctx.author
		userJson = self.checkUserExistRoutine(user)

		userS = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), userJson["balance"])
		card = certif.generateMoneyCard(userS, ggr_utilities.serverIcon(ctx.author))
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def topwad(self, ctx):
		ggr_utilities.logger(ctx, ctx.message.content)
		try:
			userJson1, userJson2, userJson3 = self.findUserMaxBalanceRoutine()
			u1 = await self.bot.fetch_user(userJson1["id"])
			u2 = await self.bot.fetch_user(userJson2["id"])
			u3 = await self.bot.fetch_user(userJson3["id"])

			userStruct1 = userStruct(u1.name, u1.discriminator, ggr_utilities.userIcon(u1), userJson1["balance"])
			userStruct2 = userStruct(u2.name, u2.discriminator, ggr_utilities.userIcon(u2), userJson2["balance"])
			userStruct3 = userStruct(u3.name, u3.discriminator, ggr_utilities.userIcon(u3), userJson3["balance"])

			card = certif.generateMoneyPodium(userStruct1, userStruct2, userStruct3, ggr_utilities.serverIcon(ctx.author), ctx.guild.name)

			await ctx.send(file = discord.File('tmp/card_podium_filled.png'))
		except:
			ggr_utilities.logger(None, "Error generating the topwaf card")
			await ctx.send("Il n'y a pas assez d'actionnaires du WAD dans la banque !")

	@commands.command()
	async def buy(self, ctx):
		"""La boutique !"""
		ggr_utilities.logger(ctx, ctx.message.content)
		user = self.checkUserExistRoutine(ctx.author)

	######################### SHELL COMMANDS #########################

	@Com.add_method(Com.Shell)
	def do_changeBalance(arg):
		'Return the verion hash number'
		#TODO: parcer les argument et verifier d'avoir selectUser
		print(Com.workingId)
		if (Com.workingType == Com.ObjectComType.USER):
			print("user selected")
		else :
			print("user NOT selected")

		#Eco.changeBallanceRoutine()	
	
	############################ ROUTINES ############################

	def loadFromFileRoutine(self):
		with open('economy.json', encoding='utf-8') as json_file:
			self.saveFile = json.load(json_file)

	def saveToFileRoutine(self):
		ggr_utilities.logger(None, "Saving to file the new balance of an user")
		with open('economy.json', 'w') as json_file:
			json.dump(self.saveFile, json_file)
	
	@classmethod
	def checkUserExistRoutine(self, user):
		ggr_utilities.logger(None, "Check if user exist.")
		self.loadFromFileRoutine(self)
		for u in self.saveFile:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger(None, "User " + user.name + " not found adding him/her to the economy file")
		newUserJson = {"name": user.name , "id": user.id, "balance": 1 }

		self.saveFile.append(newUserJson)
		self.saveToFileRoutine(self)
		return newUserJson

	@classmethod
	def changeBallanceRoutine(self, user, diff):
		self.checkUserExistRoutine(user)
		ggr_utilities.logger(None, "add " + str(diff) + " wads to " + user.name)
		self.loadFromFileRoutine(self)
		for u in self.saveFile:
			if u["name"] == user.name:
				u["balance"] += diff
		self.saveToFileRoutine(self)

	@classmethod
	def findUserMaxBalanceRoutine(self):
		ggr_utilities.logger(None, "Find max balance.")
		self.loadFromFileRoutine(self)

		self.saveFile.sort(key = lambda user:user["balance"], reverse = True)
		
		u1, u2, u3 = {"name": "nobody" , "id": 1, "balance": 1 }
		lenght = len(self.saveFile)
		if (lenght > 0):
			u1 = self.saveFile[0]
		if (lenght > 1):
			u2 = self.saveFile[1]
		if (lenght > 2):
			u3 = self.saveFile[2]		
		return u1, u2, u3

def setup(bot):
	bot.add_cog(Eco(bot))
