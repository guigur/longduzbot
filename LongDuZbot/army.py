import discord
from discord.ext import commands
import random
import time
import datetime
import requests
import math
import json

import ggr_utilities
import ggr_emotes
import certif
import eco

class Army(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.timeReady = 0
		self.loadFromFile()

	def loadFromFile(self):
		with open('maitre.json', encoding='utf-8') as json_file:
			self.saveFile = json.load(json_file)

	def saveToFile(self):
		ggr_utilities.logger(None, "Saving to file the new master")
		with open('maitre.json', 'w') as json_file:
			json.dump(self.saveFile, json_file)
			
	def loadFromFileCoolDown(self):
		with open('army_cool_down.json', encoding='utf-8') as json_file:
			self.saveFileCoolDown = json.load(json_file)

	def saveToFileCoolDown(self):
		ggr_utilities.logger(None, "Saving to file army cool down")
		with open('army_cool_down.json', 'w') as json_file:
			json.dump(self.saveFileCoolDown, json_file)

	def spawnArmy(self):
		army = ""
		armynbr = random.randint(10, 40)
		armyGold = 0
		for x in range(0, armynbr):
			doreeNbr = random.randint(0, 2999)
			if doreeNbr < 10:
				army += ggr_emotes.Saloperiedoree
				armynbr += 9 #Une saloperie doree vaut 10 saloperies classiques 
				armyGold += 1
			else:
				armymbr = random.randint(0, 100)
				if armymbr <= 49:
					army += ggr_emotes.Ulian
				elif armymbr == 50:
					army += ggr_emotes.Guogur
				elif armymbr >= 51:
					army += ggr_emotes.Moth
		return [army, armynbr, armyGold]

	def checkUserCoolDownExist(self, user):
		ggr_utilities.logger(None, "Check if user cool down exist.")
		self.loadFromFileCoolDown()
		for u in self.saveFileCoolDown:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger(None, "User " + user.name + " not found adding him/her to cool down file")
		newUserJson = {"name": user.name , "id": user.id, "date": time.time() }

		self.saveFileCoolDown.append(newUserJson)
		self.saveToFileCoolDown()
		return newUserJson

	@commands.command()
	async def maitre(self, ctx):
		"""Affiche le maître des saloperies et son record."""
		ggr_utilities.logger(ctx, ctx.message.content)
		msg = "Le maître des saloperie est **" + self.saveFile['maitre']['user'] + "** avec un score de **" + str(self.saveFile['maitre']['best']) + "** saloperies invoqués"
		await ctx.send(msg)

	@commands.command()
	async def army(self, ctx):
		"""Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires."""
		ggr_utilities.logger(ctx, ctx.message.content)
		timeUser = self.checkUserCoolDownExist(ctx.author)["date"]
		if (time.time() >= timeUser):
			for u in self.saveFileCoolDown:
				if u["name"] == ctx.author.name:
					u["date"] =  time.time() + 300 #5min

			self.saveToFileCoolDown()

			retarmy = self.spawnArmy()
			army = retarmy[0]
			armytotmembers = retarmy[1]
			armyGold = retarmy[2]
			await ctx.send(army)
			for emojinmb in ggr_utilities.numbersToEmojis(armytotmembers):
				await ctx.message.add_reaction(emojinmb)
			if armyGold > 0:
				await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " WADs**")
				await ctx.message.add_reaction(ggr_emotes.WAD)
				eco.Eco.changeBallance(ctx.author, armyGold)
		else:
			await ctx.send("Votre armée de saloperies n'est pas prête.\nRéessayez dans **" + str(math.trunc(self.checkUserCoolDownExist(ctx.author)["date"] - time.time())) + "** secondes.")
			await ctx.message.add_reaction("❌")


	@commands.command()
	async def megaarmy(self, ctx):
		"""Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes."""
		ggr_utilities.logger(ctx, ctx.message.content)
		armytotmembers = 0
		armyGold = 0
		if ctx.author.name != self.saveFile['maitre']['user']:
			if time.time() > self.timeReady:
				ggr_utilities.logger(None, "User " + ctx.author.name + " summoned a megaarmy")
				self.timeReady = time.time() + random.randint(900, 1500) #entre 15 et 25 min

				armyLines = random.randint(5, 20)
				for x in range(0, armyLines):
					retarmy = self.spawnArmy()
					army = retarmy[0]
					armytotmembers += retarmy[1]
					armyGold += retarmy[2]

					await ctx.send(army)
				for emojinmb in ggr_utilities.numbersToEmojis(armyLines):
					await ctx.message.add_reaction(emojinmb)
				ggr_utilities.logger(None, "User " + ctx.author.name + " summoned " + str(armytotmembers) + " saloperies")
				await ctx.send("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
				if armyGold > 0:
					await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " WADs**")
					await ctx.message.add_reaction(ggr_emotes.WAD)
					eco.Eco.changeBallance(ctx.author, armyGold)
				if armytotmembers > self.saveFile['maitre']['best']:
					ggr_utilities.logger(None, "User " + ctx.author.name + " is now the master of saloperies")
					user = ctx.author
					#TODO: Remove the old master
					#oldmaitre = user.guild.members() #199222032787963904) #user = client.get_user()
					#await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #remove the role

					self.saveFile['maitre']['best'] = armytotmembers;
					self.saveFile['maitre']['user'] = ctx.author.name
					self.saveFile['maitre']['userid'] = ctx.author.id
					self.saveFile['maitre']['date'] = datetime.datetime.timestamp(datetime.datetime.now())

					self.saveToFile()
					await ctx.send("Félicitations " + user.mention + " vous êtes le nouveau **Maître des Saloperies**")
					url = ctx.author.avatar_url_as(format='png')
					picture = certif.certifGen(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
					await ctx.send(file=discord.File('tmp/certif_filled.png'))
					await ctx.send("Ce certificat prouve votre titre de **Maître des Saloperies**\nN'hésitez pas à mentionner ce titre prestigieux sur votre CV.")
					try:
						await user.add_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies"))
					except discord.Forbidden:
						pass

				else:
					await ctx.send("Bien mais il y a mieux")
			else:
				await ctx.send("La méga armée de saloperies n'est pas prête.\nRéessayez dans quelques minutes.")
				await ctx.message.add_reaction("❌")
		else:
			await ctx.send("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(self.saveFile['maitre']['best']) + "** Saloperies.")


def setup(bot):
	bot.add_cog(Army(bot))
