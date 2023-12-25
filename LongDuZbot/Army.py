import discord
from discord.ext import commands
import random
import time
import datetime
import requests
import math
import json
import os
import ggr_utilities, ggr_emotes
import certif
import Eco, Com, Database

from collections import namedtuple 

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

class Army(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.timeReady = 0

		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database cog", self, ggr_utilities.LogType.ERROR)

		self.eco = self.bot.get_cog('Eco')
		if self.eco is None:
			ggr_utilities.logger("Missing Eco cog", ggr_utilities.LogType.ERROR)
######################## DISCORD COMMANDS ########################

	@commands.command()
	async def maitre(self, ctx):
		"""Affiche le maître des saloperies et son record."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		DBMaitre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.MAITRE)
		if (DBMaitre and ggr_utilities.checkIfIdValid(DBMaitre[1])):
			user = await self.bot.fetch_user(DBMaitre[1])
		else:
			await ctx.send("Personne n'est maitre pour l'instant")
			return
		ustruct = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), DBMaitre[6])
		card = certif.cardSaloperieBestWorst(ustruct, ggr_utilities.userIcon(user), ggr_utilities.serverIcon(ctx.guild), certif.BestWorst.best) #user n'a pas d'argument guild
		
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def jeanfoutre(self, ctx):
		"""Affiche le jean-foutre des saloperies et son score."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		DBJeanfoutre= self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE)
		if (DBJeanfoutre and ggr_utilities.checkIfIdValid(DBJeanfoutre[1])):
			user = await self.bot.fetch_user(DBJeanfoutre[1])
		else:
			await ctx.send("Personne n'est le jean-foutre pour l'instant")
			return
		ustruct = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), DBJeanfoutre[6])
		card = certif.cardSaloperieBestWorst(ustruct, ggr_utilities.userIcon(user), ggr_utilities.serverIcon(ctx.guild), certif.BestWorst.worst) #user n'a pas d'argument guild
		
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def armydory(self, ctx):
		"""Affiche une belle armée de soldats dorés."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		armynbr = random.randint(10, 60)
		army = ""
		for x in range(0, armynbr):
			army += ggr_emotes.Saloperiedoree
		await ctx.send(army)

	@commands.command()
	async def army(self, ctx):
		"""Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		timeUser = self.hasUserCoolDownRoutine(ctx.author)["date"]
		if (time.time() >= timeUser):
			for u in self.saveFileCoolDown:
				if u["name"] == ctx.author.name:
					u["date"] =  time.time() + 300 #5min
			#game = discord.Game("envoyer une armée")
			#await bot.change_presence(status=discord.Status.online, activity=game)
			self.saveToFileCoolDownRoutine()

			retarmy = self.spawnArmyRoutine()
			army = retarmy[0]
			armytotmembers = retarmy[1]
			armyGold = retarmy[2]
			await ctx.send(army)

			self.database.addDBArmy(ctx.author, ctx.message.guild, time.time(), ctx.message.content, armytotmembers, armyGold)

			for emojinmb in ggr_utilities.numbersToEmojis(armytotmembers):
				await ctx.message.add_reaction(emojinmb)
			if armyGold > 0:
				await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " " + Eco.moneyName(armyGold) + "**")
				await ctx.message.add_reaction(ggr_emotes.WAD)
				##self.eco.changeBallanceRoutine(ctx.author, armyGold) ##TODO: change call to eco ##########==
				self.database.changeDBBalanceMoney(ctx.author, ctx.guild, armyGold)

		else:
			await ctx.send("Votre armée de saloperies n'est pas prête.\nRéessayez dans **" + str(math.trunc(self.hasUserCoolDownRoutine(ctx.author)["date"] - time.time())) + "** secondes.")
			await ctx.message.add_reaction("❌")

	@commands.command()
	async def megaarmy(self, ctx):
		"""Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		armytotmembers = 0
		armyGold = 0
		
		DBMaitre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.MAITRE)
		DBJeanfoutre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE)

		if (DBMaitre is None or ctx.author.id != DBMaitre[1]):
			if (time.time() > self.timeReady):
				#game = discord.Game("envoyer une megaarmée")
				#await bot.change_presence(status=discord.Status.online, activity=game)

				ggr_utilities.logger("User " + ctx.author.name + " summoned a megaarmy", self)
				self.timeReady = time.time() + random.randint(900, 1500) #entre 15 et 25 min

				armyLines = random.randint(5, 20)
				for x in range(0, armyLines):
					retarmy = self.spawnArmyRoutine()
					army = retarmy[0]
					armytotmembers += retarmy[1]
					armyGold += retarmy[2]

					await ctx.send(army)
				for emojinmb in ggr_utilities.numbersToEmojis(armyLines):
					await ctx.message.add_reaction(emojinmb)
				ggr_utilities.logger("User " + ctx.author.name + " summoned " + str(armytotmembers) + " saloperies", self)

				megaarmyID = self.database.addDBMegaArmy(ctx.author, ctx.guild, time.time(), ctx.message.content, armyLines, armytotmembers, armyGold)

				await ctx.send("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
				if armyGold > 0:
					await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " " + Eco.moneyName(armyGold) + "**")
					await ctx.message.add_reaction(ggr_emotes.WAD)
					#self.eco.changeBallanceRoutine(ctx.author, armyGold) ##TODO: change call to eco ##########==
					self.database.changeDBBalanceMoney(ctx.author, ctx.guild, armyGold)

				if (DBMaitre is None or armytotmembers > DBMaitre[6]):
					await self.grantMasterRoutine(ctx, armytotmembers, megaarmyID)
				elif (DBJeanfoutre is None or armytotmembers < DBJeanfoutre[6]):
					await self.grantWorstRoutine(ctx, armytotmembers, megaarmyID)
				else:
					#TODO: mettre differentes reactions en fonction du score
					await ctx.send("Bien mais il y a mieux")
			else:
				await ctx.send("La méga armée de saloperies n'est pas prête.\nRéessayez dans quelques minutes.")
				await ctx.message.add_reaction("❌")
		else:
			await ctx.send("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(DBMaitre[6]) + "** Saloperies.")
	
	######################### SHELL COMMANDS #########################

	############################ ROUTINES ############################

	#TODO: make a function with this stuff
	def loadFromFileCoolDownRoutine(self):
		filename = "army_cool_down.json"
		if os.path.exists(filename):
			mode = "r"
		else:
			mode = "w+"
			ggr_utilities.logger(filename + " is non existant. Creating", self)

		with open(filename, mode, encoding='utf-8') as json_file:
			filesize = os.path.getsize(filename)
			# print(str(filesize))
			if filesize == 0:
				ggr_utilities.logger(filename + " is empty. Initializing", self)
				self.saveFileCoolDown = json.loads("[]")
			else:
				self.saveFileCoolDown = json.load(json_file)

	def saveToFileCoolDownRoutine(self):
		ggr_utilities.logger("Saving to file army cool down", self)
		with open('army_cool_down.json', 'w') as json_file:
			json.dump(self.saveFileCoolDown, json_file)

	def spawnArmyRoutine(self):
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
					army += ggr_emotes.Guigor
				elif armymbr >= 51:
					army += ggr_emotes.Moth
		return [army, armynbr, armyGold]

	def hasUserCoolDownRoutine(self, user):
		ggr_utilities.logger("Check if user cool down exist.", self)
		self.loadFromFileCoolDownRoutine()
		for u in self.saveFileCoolDown:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger("User " + user.name + " not found adding him/her to cool down file", self)
		newUserJson = {"name": user.name , "id": user.id, "date": time.time() }

		self.saveFileCoolDown.append(newUserJson)
		self.saveToFileCoolDownRoutine()
		return newUserJson

	async def grantMasterRoutine(self, ctx, armytotmembers, megaarmyID):
		ggr_utilities.logger("User " + ctx.author.name + " is now the master of saloperies", self)
		user = ctx.author
		guild = ctx.message.guild
		role = await ggr_utilities.getRole(guild)
		await ggr_utilities.supromote(ctx)

		DBMaitre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.MAITRE)
		DBJeanfoutre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE)

		if (DBMaitre is None):
			firstMaitre = True
		else:
			oldMaitreID = DBMaitre[1] 
			try:
				oldMaitre = await self.bot.fetch_user(oldMaitreID)
				firstMaitre = False
			except:
				firstMaitre = True
			
		self.database.setDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.MAITRE, ctx.author, ctx.guild, time.time(), armytotmembers, megaarmyID)
		
		if (DBJeanfoutre is None or armytotmembers < DBJeanfoutre[6]): #if the worst has not been choosen yetm we lower the minimum to the best score yet
			self.database.setDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE, ggr_utilities.dummyUser, ctx.guild, time.time(), armytotmembers, megaarmyID)

		#self.saveDataToFileRoutine() ############
		await ctx.send("Félicitations " + user.mention + " vous êtes le nouveau " + role.mention)
		if (not firstMaitre):
			await ctx.send("Désolé " + oldMaitre.mention + ", il va falloir faire mieux !")

		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifMaster(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.send(file=discord.File('tmp/certif_best_filled.png'))
		await ctx.send("Ce certificat prouve votre presigieux titre de " + role.mention + "\nN'hésitez pas à mentionner ce titre prestigieux sur votre CV.")

	async def grantWorstRoutine(self, ctx, armytotmembers, megaarmyID):
		ggr_utilities.logger("User " + ctx.author.name + " is now the good-for-nothing of saloperies", self)
		user = ctx.author

		self.database.setDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE, ctx.author, ctx.guild, time.time(), armytotmembers, megaarmyID)

		await ctx.send("Félicitations " + user.mention + " vous êtes le nouveau **Jean-foutre des Saloperies**")
		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifBitch(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.send(file=discord.File('tmp/certif_worst_filled.png'))
		await ctx.send("Ce certificat prouve votre titre de **Jean-foutre des Saloperies**\nVous êtes un bon à rien, un cloporte, un ectoplasme à roulettes. Bref, pas ouf quoi.")

def setup(bot):
	bot.add_cog(Army(bot))
