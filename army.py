import discord
from discord.ext import commands
import random
import time
import datetime
import requests

import json

import ggr_utilities
import ggr_emotes
import certif

timeReady = 0

with open('maitre.json', encoding='utf-8') as json_file:
	saveFile = json.load(json_file)

def spawnArmy():
	army = ""
	armynbr = random.randint(10, 40)
	for x in range(0, armynbr):
		armymbr = random.randint(0, 1)
		if armymbr == 0:
			army += ggr_emotes.Ulian
		else:
			army += ggr_emotes.Moth
	return [army, armynbr]



def saveToFile():
	print("Saving to file")
	with open('maitre.json', 'w') as json_file:
		json.dump(saveFile, json_file)

class Army(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def maitre(self, ctx):
		"""Affiche le maître des saloperies et son record."""
		ggr_utilities.logger(ctx, ctx.message.content)
		msg = "Le maître des saloperie est **" + saveFile['maitre']['user'] + "** avec un score de **" + str(saveFile['maitre']['best']) + "** saloperies invoqués"
		await ctx.send(army)

	@commands.command()
	async def army(self, ctx):
		"""Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires."""
		ggr_utilities.logger(ctx, ctx.message.content)
		army = spawnArmy()[0]
		await ctx.send(army)

	@commands.command()
	async def megaarmy(self, ctx):
		"""Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes."""
		ggr_utilities.logger(ctx, ctx.message.content)
		armytotmembers = 0
		global timeReady
		if ctx.author.name != saveFile['maitre']['user']:
			if time.time() > timeReady:
				print(ggr_utilities.pDT() + "User " + ctx.author.name + " summoned a megaarmy")
				timeReady = time.time() + 1200
				armyLines = random.randint(5, 20)
				for x in range(0, armyLines):
					retarmy = spawnArmy()
					army = retarmy[0]
					armytotmembers += retarmy[1]
					await ctx.send(army)
				for emojinmb in ggr_utilities.numbersToEmojis(armyLines):
					await ctx.message.add_reaction(emojinmb)
				print(ggr_utilities.pDT() + "User " + ctx.author.name + " summoned " + str(armytotmembers))
				await ctx.send("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
				
				
				if armytotmembers > saveFile['maitre']['best']:
					print(ggr_utilities.pDT() + "User " + ctx.author.name + " is now the master")

					user = ctx.author

					#oldmaitre = user.guild.members() #199222032787963904) #user = client.get_user()
					#await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #remove the role

					saveFile['maitre']['best'] = armytotmembers;
					saveFile['maitre']['user'] = ctx.author.name
					saveFile['maitre']['userid'] = ctx.author.id
					saveFile['maitre']['date'] = datetime.datetime.timestamp(datetime.datetime.now())


					saveToFile()
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
			await ctx.send("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(saveFile['maitre']['best']) + "** Saloperies.")


def setup(bot):
	bot.add_cog(Army(bot))
