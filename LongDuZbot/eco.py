import discord
import os
import certif
from discord.ext import commands
from discord.utils import get

import json

import ggr_utilities
import ggr_emotes

class Eco(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def loadFromFile(self):
		with open('economy.json', encoding='utf-8') as json_file:
			self.saveFile = json.load(json_file)

	def saveToFile(self):
		ggr_utilities.logger(None, "Saving to file the new balance of an user")
		with open('economy.json', 'w') as json_file:
			json.dump(self.saveFile, json_file)
	
	@classmethod
	def checkUserExist(self, user):
		ggr_utilities.logger(None, "Check if user exist.")
		self.loadFromFile(self)
		for u in self.saveFile:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger(None, "User " + user.name + " not found adding him/her to the economy file")
		newUserJson = {"name": user.name , "id": user.id, "balance": 1 }

		self.saveFile.append(newUserJson)
		self.saveToFile(self)
		return newUserJson

	@classmethod
	def changeBallance(self, user, diff):
		self.checkUserExist(user)
		ggr_utilities.logger(None, "add " + str(diff) + " wads to " + user.name)
		self.loadFromFile(self)
		for u in self.saveFile:
			if u["name"] == user.name:
				u["balance"] += diff
		self.saveToFile(self)

	@commands.command()
	async def wad(self, ctx, *arg):
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""
		ggr_utilities.logger(ctx, ctx.message.content)
		
		if not arg:
			user = self.checkUserExist(ctx.author)
		else:
			members = ctx.guild.members
			for member in members:
				await ctx.send(member)
			#user = await get(ctx.guild.members, name='guigur')
			return
			#user = self.checkUserExist(ctx)
		userImg, guildImg = ggr_utilities.userServerIcon(ctx) 
		card = certif.generateMoneyCard(userImg, guildImg, ctx, user["balance"])
		await ctx.send(file=discord.File('tmp/card_filled.png'))
		#await ctx.send("**" + user["name"] + "** possède **" + str(user['balance']) + "** WADs en banque.")

	@commands.command()
	async def buy(self, ctx, *arg):
		"""La boutique !"""
		ggr_utilities.logger(ctx, ctx.message.content)
		shopItemAvailable = ["taunt (1 WAD)"]

		if not arg:
			await ctx.send("Les différents items disponibles sont les suivants:")
			await ctx.send(' '.join(shopItemAvailable)) 
		else:
			if (arg[0] == "taunt"):
				#si asser d'argent, alors crediter l objet ou depenser le taunt
				await ctx.send("") 

			else:
				await ctx.send("Cet article n'existe pas") 

		#check if no argument

		#if no arguments return the list of the goods availables
		user = self.checkUserExist(ctx.author)

		

def setup(bot):
	bot.add_cog(Eco(bot))
