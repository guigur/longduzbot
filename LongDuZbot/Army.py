import discord
from discord.ext import commands
import random
import time
import datetime
import requests
import math
import json
import os
# import asyncio
import threading
import ggr_utilities, ggr_emotes
import certif
import Eco, Com, Database

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpli
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

from collections import namedtuple 

userStruct = namedtuple("userStruct", ["name", "discriminator", "icon", "balance"])

class Army(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.add_listener(self.on_reaction_add, 'on_reaction_add')
		self.timeReady = 0
		self.coolDownTime = 1 #300 #5min

		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database Cog", self, ggr_utilities.LogType.CRIT)

		self.eco = self.bot.get_cog('Eco')
		if self.eco is None:
			ggr_utilities.logger("Missing Eco Cog", self, ggr_utilities.LogType.CRIT)

		self.random_precision = 6
		self.random_max_int = 10 ** self.random_precision

		self.saloperies = [
		{"emote": ggr_emotes.Ulian, 			"name": "Ulian", 			"commonness": 1,		"effect": self.effetCollocU},
		{"emote": ggr_emotes.Polpoth, 			"name": "Polpoth",	 		"commonness": 0.1, 		"effect": None},
		{"emote": ggr_emotes.Guigor, 			"name": "Guigor", 			"commonness": 0.1, 		"effect": None},
		{"emote": ggr_emotes.Salstealthy, 		"name": "Salstealthy", 		"commonness": 0.1,	 	"effect": None},
		{"emote": ggr_emotes.Culian, 			"name": "Culian", 			"commonness": 0.15, 	"effect": self.effetCullocU},
		{"emote": ggr_emotes.Culoth, 			"name": "Culoth", 			"commonness": 0.15, 	"effect": self.effetCullocM},
		{"emote": ggr_emotes.Brandon,			"name": "Brandon", 			"commonness": 0.1, 		"effect": None},
		{"emote": ggr_emotes.Saloperiedoree,	"name": "Saloperiedoree", 	"commonness": 0.01, 	"effect": self.effetSaloperieDoree},
		{"emote": ggr_emotes.Moth, 				"name": "Moth", 			"commonness": 1, 		"effect": self.effetCollocM}
		]
		self.init_drop_saloperies()

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " Cog Unloaded!" , self, None, ggr_utilities.LogType.WARN)

######################## DISCORD REACTIONS ########################

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload): #on_reaction_add does not work
		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
		reaction = discord.utils.get(message.reactions, emoji="👍")
		user = payload.member
		print(message)
		print(reaction)
		print(user)

######################## DISCORD COMMANDS ########################
	def effetSaloperieDoree(self, armyMembers):
		return(+9, +1, f"{armyMembers[-1]["emote"]}: \"Saloperie dorée\" -> +10 saloperies, +1 WAD\n")

	def effetCollocU(self, armyMembers):
		if (len(armyMembers) > 1):
			if (armyMembers[-2]["name"] == "Moth"):
				return(+1, 0, f"{armyMembers[-2]["emote"]}+{armyMembers[-1]["emote"]}: \"effet colloc\" -> +1 saloperie\n")
		return(0, 0, "")
	
	def effetCollocM(self, armyMembers):
		if (len(armyMembers) > 1):
			if (armyMembers[-2]["name"] == "Ulian"):
				return(+1, 0, f"{armyMembers[-2]["emote"]}+{armyMembers[-1]["emote"]}: \"effet colloc\" -> +1 saloperie\n")
		return(0, 0, "")

	def effetCullocU(self, armyMembers):
		if (len(armyMembers) > 1):
			if (armyMembers[-2]["name"] == "Culoth"):
				return(-1, 0, f"{armyMembers[-2]["emote"]}+{armyMembers[-1]["emote"]}: \"effet culloc\" -> -1 saloperie\n")
		return(0, 0, "")
	
	def effetCullocM(self, armyMembers):
		if (len(armyMembers) > 1):
			if (armyMembers[-2]["name"] == "Culian"):
				return(-1, 0, f"{armyMembers[-2]["emote"]}+{armyMembers[-1]["emote"]}: \"effet culloc\" -> -1 saloperie\n")
		return(0, 0, "")
	
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
		print(ctx.message.id) #########################################################################################
		"""Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		timeUser = self.hasUserCoolDownRoutine(ctx.author)["date"]
		if (time.time() >= timeUser):
			for u in self.saveFileCoolDown:
				if u["name"] == ctx.author.name:
					u["date"] =  time.time() + self.coolDownTime #5min
			#game = discord.Game("envoyer une armée")
			#await bot.change_presence(status=discord.Status.online, activity=game)
			self.saveToFileCoolDownRoutine()

			retarmy = self.spawnArmyRoutine()
			army = retarmy[0]
			armytotmembers = retarmy[1]
			armyGold = retarmy[2]
			await ctx.send(army)
			if (retarmy[3] != ""):
				await ctx.send(f"||{retarmy[3]}||")


			self.database.addDBArmy(ctx.author, ctx.message.guild, time.time(), ctx.message.content, armytotmembers, armyGold)

			for emojinmb in ggr_utilities.numbersToEmojis(armytotmembers):
				await ctx.message.add_reaction(emojinmb)
			if armyGold > 0:
				await ctx.reply("Cette armée vous rapporte **" + str(armyGold) + " " + Eco.moneyName(armyGold) + "**")
				await ctx.message.add_reaction(ggr_emotes.WAD)
				##self.eco.changeBallanceRoutine(ctx.author, armyGold) ##TODO: change call to eco ##########==
				self.database.changeDBBalanceMoney(ctx.author, ctx.guild, armyGold)

		else:
			await ctx.reply("Votre armée de saloperies n'est pas prête.\nRéessayez dans **" + str(math.trunc(self.hasUserCoolDownRoutine(ctx.author)["date"] - time.time())) + "** secondes.")
			await ctx.message.add_reaction("❌")
		await ctx.message.add_reaction("❓")

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
				armyDesc = []
				for x in range(0, armyLines): #the megaarmy
					retarmy = self.spawnArmyRoutine()
					army = retarmy[0]
					armytotmembers += retarmy[1]
					armyGold += retarmy[2]
					armyDesc.append(retarmy[3])
					await ctx.send(army)

				for emojinmb in ggr_utilities.numbersToEmojis(armyLines): #emojis number lines
					await ctx.message.add_reaction(emojinmb)
		
				for i, d in enumerate(armyDesc): #desciption
					if (d != ""):
						await ctx.send(f"ligne{i+1}\n||{d}||")

				ggr_utilities.logger("User " + ctx.author.name + " summoned " + str(armytotmembers) + " saloperies", self)

				megaarmyID = self.database.addDBMegaArmy(ctx.author, ctx.guild, time.time(), ctx.message.content, armyLines, armytotmembers, armyGold)

				await ctx.reply("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
				if armyGold > 0:
					await ctx.reply("Cette armée vous rapporte **" + str(armyGold) + " " + Eco.moneyName(armyGold) + "**")
					await ctx.message.add_reaction(ggr_emotes.WAD)
					#self.eco.changeBallanceRoutine(ctx.author, armyGold) ##TODO: change call to eco ##########==
					self.database.changeDBBalanceMoney(ctx.author, ctx.guild, armyGold)

				if (DBMaitre is None or armytotmembers > DBMaitre[6]):
					await self.grantMasterRoutine(ctx, armytotmembers, megaarmyID)
				elif (DBJeanfoutre is None or armytotmembers < DBJeanfoutre[6]):
					await self.grantWorstRoutine(ctx, armytotmembers, megaarmyID)
				else:
					#TODO: mettre differentes reactions en fonction du score
					await ctx.reply("Bien mais il y a mieux")
				await ctx.message.add_reaction("❓")
			else:
				await ctx.reply("La méga armée de saloperies n'est pas prête.\nRéessayez dans quelques minutes.")
				await ctx.message.add_reaction("❌")
		else:
			await ctx.reply("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(DBMaitre[6]) + "** Saloperies.")

	@commands.command()
	async def drop(self, ctx):
		data = {"title": "Longduzbot drop (< may 2024)",
		"sizes": [], "labels": []}

		for s in self.saloperies:
			data["sizes"].append(s["drop"])
			data["labels"].append(s["name"])
			
		self.draw_piechart_drop(data)
		await ctx.send(file = discord.File("tmp/drop.png"))

	@commands.command()
	async def olddrop(self, ctx):
		data = {"title": "Longduzbot old drop (> may 2024)",
		  		"sizes": [10/3000, 50/101, 1/101, 50/101] ,
		  		"labels": ["Saloperiedoree", "Ulian", "Guigor", "Moth"]}

		self.draw_piechart_drop(data)
		await ctx.send(file = discord.File("tmp/drop.png"))

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

	def init_drop_saloperies(self):
		total_commonness = 0

		for s in self.saloperies:
			total_commonness += s["commonness"]
		
		prev = 0
		for sp in self.saloperies:
			drop = sp["commonness"]/total_commonness
			sp["drop"] = float(f"{(drop):.{self.random_precision}f}") 
			stop = (sp["drop"] * self.random_max_int) + prev
			sp["start"] = prev
			sp["stop"] = stop
			prev = stop
			# print("common ",sp["commonness"], " drop ", sp["drop"])

	def pickSaloperie(self):
		number = random.randint(0, self.random_max_int)
		for s in self.saloperies:
			if (number >= s["start"] and number < s["stop"]):
				# print(f'GOT EM! numb: {number} | {s["name"]}: {s["start"]} -> {s["stop"]} | {s["drop"]}')
				return s
		print("error, adding ulian")
		return self.saloperies[0] #if error

	def draw_piechart_drop(self, data):

		fg_color = "#ffffff"
		bg_color = "#2F3136"
		# emote = mpli.imread("culoth.png")
		plt.subplots_adjust(wspace=500)

		fig, ax = plt.subplots(facecolor=bg_color)
		# plt.figure(figsize=(8, 6))

		legend_data = []
		for i, d in enumerate(data["labels"]):
			legend_data.append(f"{d} ({data["sizes"][i]*100:.2f}%)")

		patches, texts =  ax.pie(data["sizes"], labels=data["labels"], startangle=180, labeldistance=1.05, frame=False,
		wedgeprops = {"linewidth": 1, "edgecolor": "white"})
		plt.setp(texts, color='white')

		# plt.legend(fig, labels, loc="best")

		# imagebox = OffsetImage(emote, zoom=0.2)
		# ab = AnnotationBbox(imagebox, (1, 1), xycoords='axes fraction', frameon=False, pad=0)
		# ab.xybox = (1, 1)
		#ax.add_artist(ab)

		# patches, texts = plt.pie(sizes, colors=colors, startangle=90)
		# plt.legend(patches, labels, loc="best")

		ax.legend(patches, legend_data, loc= "lower left",  bbox_to_anchor=(-0.35, -0.1))
		ax.set_title(data["title"], color=fg_color, fontsize=20)
		plt.savefig('tmp/drop.png')

	async def on_reaction_add(self, reaction: discord.Reaction, user):
		print(f'User {user} added reaction {reaction} in channel {reaction.message.channel}')
		# await bot_channel.send(content=f"A rating of {reaction} was placed in {reaction.message.channel} for link {reaction.message.content}")

	def spawnArmyRoutine(self):
		armyMembers = []
		effectsDesc = ""
		armyEffect = 0
		armynbr = random.randint(10, 40)
		armyGold = 0
		for x in range(0, armynbr):
			armyMember = self.pickSaloperie()
			armyMembers.append(armyMember)

			if (armyMember["effect"] != None):
				effects = armyMember["effect"](armyMembers)
				armyEffect += effects[0]
				armyGold += effects[1]
				effectsDesc += effects[2]

			# if wadProbaNbr < 10:
			# 	army += ggr_emotes.Saloperiedoree
			# 	armynbr += 9 #Une saloperie doree vaut 10 saloperies classiques 
			# 	armyGold += 1

		armyEmotes = ""
		for e in armyMembers:
			armyEmotes += e["emote"]

		print(armynbr, armyEffect, armyGold)
		print(effectsDesc)
		return [armyEmotes, armynbr + armyEffect, armyGold, effectsDesc]

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
		# guild = ctx.message.guild
		# role = await ggr_utilities.getRole(guild, role_meta="master")
		role = await ggr_utilities.supromote(ctx, role_meta="master")

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
		await ctx.reply("Félicitations " + user.mention + " vous êtes le nouveau " + role.mention)
		if (not firstMaitre):
			await ctx.send("Désolé " + oldMaitre.mention + ", il va falloir faire mieux !")

		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifMaster(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.reply("Ce certificat prouve votre presigieux titre de " + role.mention + "\nN'hésitez pas à mentionner ce titre prestigieux sur votre CV.",
			file=discord.File('tmp/certif_best_filled.png'))

	async def grantWorstRoutine(self, ctx, armytotmembers, megaarmyID):
		ggr_utilities.logger("User " + ctx.author.name + " is now the good-for-nothing of saloperies", self)
		user = ctx.author
		role = await ggr_utilities.supromote(ctx, role_meta="worst")

		DBJeanfoutre = self.database.getDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE)

		self.database.setDBMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE, ctx.author, ctx.guild, time.time(), armytotmembers, megaarmyID)

		await ctx.reply("Félicitations " + user.mention + " vous êtes le nouveau " + role.mention)
		url = ctx.author.avatar_url_as(format='png')
		picture = certif.generateCertifBitch(requests.get(url, stream=True).raw, ctx.author.name, armytotmembers)
		await ctx.reply("Ce certificat prouve votre titre de " + role.mention + "\nVous êtes un bon à rien, un cloporte, un ectoplasme à roulettes. Bref, pas ouf quoi.",
			file=discord.File('tmp/certif_worst_filled.png'))

def setup(bot):
	bot.add_cog(Army(bot))
