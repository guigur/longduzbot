import discord
from discord.ext import commands
import random
import time
import datetime
import requests
import math
import json
import os
import ggr_utilities
import ggr_emotes
import certif
import Eco
from collections import namedtuple 

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

class Army(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.timeReady = 0
		self.loadDataFromFileRoutine()

######################## DISCORD COMMANDS ########################

	@commands.command()
	async def maitre(self, ctx):
		"""Affiche le maître des saloperies et son record."""
		ggr_utilities.logger(ctx, ctx.message.content)
		#msg = "Le maître des saloperie est **" + self.data['best']['user'] + "** avec un score de **" + str(self.data['best']['score']) + "** saloperies invoqués"
		if ggr_utilities.checkIfIdValid(self.data['best']['userid']):
			user = await self.bot.fetch_user(self.data['best']['userid'])
		else:
			await ctx.send("Personne n'est maitre pour l'instant")
			return
		ustruct = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), self.data['best']['score'])
		card = certif.cardSaloperieBestWorst(ustruct, ggr_utilities.userIcon(user), ggr_utilities.serverIcon(ctx.author), certif.BestWorst.best) #user n'a pas d'argument guild
		
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def jeanfoutre(self, ctx):
		"""Affiche le jean-foutre des saloperies et son score."""
		ggr_utilities.logger(ctx, ctx.message.content)
		#msg = "Le jean-foutre des saloperie est **" + self.data['worst']['user'] + "** avec un score de minabke de **" + str(self.data['worst']['score']) + "** saloperies invoqués"
		if ggr_utilities.checkIfIdValid(self.data['worst']['userid']):
			user = await self.bot.fetch_user(self.data['worst']['userid'])
		else:
			await ctx.send("Personne n'est le jean-foutre pour l'instant")
			return
		ustruct = userStruct(user.name, user.discriminator, ggr_utilities.userIcon(user), self.data['worst']['score'])
		card = certif.cardSaloperieBestWorst(ustruct, ggr_utilities.userIcon(user), ggr_utilities.serverIcon(ctx.author), certif.BestWorst.worst) #user n'a pas d'argument guild
		
		await ctx.send(file = discord.File('tmp/card_filled.png'))

	@commands.command()
	async def armydory(self, ctx):
		"""Affiche une belle armée de soldats dorés."""
		ggr_utilities.logger(ctx, ctx.message.content)
		armynbr = random.randint(10, 60)
		army = ""
		for x in range(0, armynbr):
			army += ggr_emotes.Saloperiedoree
		await ctx.send(army)

	@commands.command()
	async def army(self, ctx):
		"""Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires."""
		ggr_utilities.logger(ctx, ctx.message.content)
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
			for emojinmb in ggr_utilities.numbersToEmojis(armytotmembers):
				await ctx.message.add_reaction(emojinmb)
			if armyGold > 0:
				await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " WADs**")
				await ctx.message.add_reaction(ggr_emotes.WAD)
				eco.Eco.changeBallance(ctx.author, armyGold)
		else:
			await ctx.send("Votre armée de saloperies n'est pas prête.\nRéessayez dans **" + str(math.trunc(self.hasUserCoolDownRoutine(ctx.author)["date"] - time.time())) + "** secondes.")
			await ctx.message.add_reaction("❌")

	##TODO remove this
	@commands.command()
	async def gm(self, ctx):
		if (ctx.author.id == 199222032787963904):
			await self.grantMasterRoutine(ctx, 596)

	@commands.command()
	async def megaarmy(self, ctx):
		"""Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes."""
		ggr_utilities.logger(ctx, ctx.message.content)
		armytotmembers = 0
		armyGold = 0
		if ctx.author.name != self.data['best']['user']:
			if time.time() > self.timeReady:
				#game = discord.Game("envoyer une megaarmée")
				#await bot.change_presence(status=discord.Status.online, activity=game)

				ggr_utilities.logger(None, "User " + ctx.author.name + " summoned a megaarmy")
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
				ggr_utilities.logger(None, "User " + ctx.author.name + " summoned " + str(armytotmembers) + " saloperies")
				await ctx.send("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
				if armyGold > 0:
					await ctx.send("Cette armée vous rapporte **" + str(armyGold) + " WADs**")
					await ctx.message.add_reaction(ggr_emotes.WAD)
					eco.Eco.changeBallance(ctx.author, armyGold)
				if armytotmembers > self.data['best']['score']:
					await self.grantMasterRoutine(ctx, armytotmembers)
				elif armytotmembers < self.data['worst']['score']:
					await self.grantWorstRoutine(ctx, armytotmembers)
				else:
					#TODO: mettre differentes reactions en fonction du score
					await ctx.send("Bien mais il y a mieux")
			else:
				await ctx.send("La méga armée de saloperies n'est pas prête.\nRéessayez dans quelques minutes.")
				await ctx.message.add_reaction("❌")
		else:
			await ctx.send("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(self.data['best']['score']) + "** Saloperies.")

############################ ROUTINES ############################

	def loadDataFromFileRoutine(self):
		with open('data.json', encoding='utf-8') as json_file:
			self.data = json.load(json_file)

	def saveDataToFileRoutine(self):
		ggr_utilities.logger(None, "Saving data")
		with open('data.json', 'w') as json_file:
			json.dump(self.data, json_file)

	#TODO: make a function with this stuff
	def loadFromFileCoolDownRoutine(self):
		filename = "army_cool_down.json"
		if os.path.exists(filename):
			mode = "r"
		else:
			mode = "w+"
			ggr_utilities.logger(None, filename + " is non existant. Creating")

		with open(filename, mode, encoding='utf-8') as json_file:
			filesize = os.path.getsize(filename)
			print(str(filesize))
			if filesize == 0:
				ggr_utilities.logger(None, filename + " is empty. Initializing")
				self.saveFileCoolDown = json.loads("[]")
			else:
				self.saveFileCoolDown = json.load(json_file)

	def saveToFileCoolDownRoutine(self):
		ggr_utilities.logger(None, "Saving to file army cool down")
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
		ggr_utilities.logger(None, "Check if user cool down exist.")
		self.loadFromFileCoolDownRoutine()
		for u in self.saveFileCoolDown:
			if u["name"] == user.name:
				return u
		ggr_utilities.logger(None, "User " + user.name + " not found adding him/her to cool down file")
		newUserJson = {"name": user.name , "id": user.id, "date": time.time() }

		self.saveFileCoolDown.append(newUserJson)
		self.saveToFileCoolDownRoutine()
		return newUserJson

	async def grantMasterRoutine(self, ctx, armytotmembers):
		ggr_utilities.logger(None, "User " + ctx.author.name + " is now the master of saloperies")
		user = ctx.author
		guild = ctx.message.guild
		role = await ggr_utilities.getRole(guild)
		await ggr_utilities.supromote(ctx)
		firstMaitre = False

		oldMaitreID = self.data['best']['userid']
		try:
			oldMaitre = await self.bot.fetch_user(oldMaitreID)
		except:
			firstMaitre = True

		self.data['best']['score'] = armytotmembers
		self.data['best']['user'] = ctx.author.name
		self.data['best']['userid'] = ctx.author.id
		self.data['best']['date'] = datetime.datetime.timestamp(datetime.datetime.now())
		
		if armytotmembers < self.data['worst']['score']: #if the worst has not been choosen yetm we lower the minimum to the best score yet
			self.data['worst']['score'] = armytotmembers

		self.saveDataToFileRoutine()
		await ctx.send("Félicitations " + user.mention + " vous êtes le nouveau " + role.mention)
		if (not firstMaitre):
			await ctx.send("Désolé " + oldMaitre.mention + ", il va falloir faire mieux !")

		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifMaster(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.send(file=discord.File('tmp/certif_best_filled.png'))
		await ctx.send("Ce certificat prouve votre presigieux titre de " + role.mention + "\nN'hésitez pas à mentionner ce titre prestigieux sur votre CV.")

	async def grantWorstRoutine(self, ctx, armytotmembers):
		ggr_utilities.logger(None, "User " + ctx.author.name + " is now the good-for-nothing of saloperies")
		user = ctx.author

		self.data['worst']['score'] = armytotmembers
		self.data['worst']['user'] = ctx.author.name
		self.data['worst']['userid'] = ctx.author.id
		self.data['worst']['date'] = datetime.datetime.timestamp(datetime.datetime.now())

		self.saveDataToFileRoutine()
		await ctx.send("Félicitations " + user.mention + " vous êtes le nouveau **Jean-foutre des Saloperies**")
		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifBitch(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.send(file=discord.File('tmp/certif_worst_filled.png'))
		await ctx.send("Ce certificat prouve votre titre de **Jean-foutre des Saloperies**\nVous êtes un bon à rien, un cloporte, un ectoplasme à roulettes. Bref, pas ouf quoi.")

def setup(bot):
	bot.add_cog(Army(bot))