import discord
from discord.ext import commands
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
	
	def changeBallance(self, user, diff):
		Eco.checkUserExist(user)
		Eco.loadFromFile()
		for u in Eco.saveFile:
			if u["name"] == user.name:
				u["balance"] += diff
		Eco.saveToFile()
		

	def checkUserExist(self, user):
		ggr_utilities.logger(None, "Check if user exist.")
		self.loadFromFile()
		for u in self.saveFile:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger(None, "User " + user.name + " not found adding him/her to the economy file")
		newUserJson = {"name": user.name , "id": user.id, "balance": 1 }

		self.saveFile.append(newUserJson)
		self.saveToFile()
		return newUserJson

	@commands.command()
	async def wad(self, ctx):
		"""Affiche le nombre de WADs que vous disposez dans la banque des WADs"""
		ggr_utilities.logger(ctx, ctx.message.content)
		
		user = self.checkUserExist(ctx.author)
		await ctx.send("**" + user["name"] + "** possède **" + str(user['balance']) + "** WADs en banque.")

def setup(bot):
	bot.add_cog(Eco(bot))