import discord
from discord.ext import commands
import requests
import cmd
import ggr_utilities
import git
from termcolor import colored
import Com
from pprint import pprint

typeDiff = { "A": {"emoji": "🆕", "text": "fichier ajouté", "color": "yellow"}, ##
			 "D": {"emoji": "❌", "text": "fichier supprimé", "color": "red"}, #
			 "R": {"emoji": "✏️", "text": "fichier renommé", "color": "magenta"}, ##
			 "M": {"emoji": "📝", "text": "fichier modifié", "color": "cyan"}, #
			 "T": {"emoji": "🥸", "text": "type de fichier modifié", "color": "grey"}, ##
			 "U": {"emoji": "🕵️", "text": "fichier non suivi", "color": "green"}} #

class Utils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " Cog Unloaded!" , self, None, ggr_utilities.LogType.WARN)

	######################## DISCORD COMMANDS ########################

	@commands.command()
	async def version(self, ctx):
		"""Affiche la version du bot."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		sha = self.gitVerisonRoutine()
		url = ggr_utilities.githubBaseUrl + "commit/" + sha
		
		embed=discord.Embed(title=discord.__name__ + " module version: " + discord.__version__, color=ggr_utilities.ggr_green)
		await ctx.send(embed=embed)
		embed=discord.Embed(title=requests.__name__ + " module version: " + requests.__version__, color=ggr_utilities.ggr_green)
		await ctx.send(embed=embed)
		embed=discord.Embed(title="commit: " + sha, url=url, color=ggr_utilities.embedUtilitiesColor)
		await ctx.send(embed=embed)

	@commands.command()
	async def diff(self, ctx):
		"""Affiche les fichiers modifies en local du bot."""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		diff = self.gitDiffRoutine()
		if (not diff):
			embed=discord.Embed(title="👍 Aucun changements locaux", color=ggr_utilities.ggr_green)
		else:
			embed=discord.Embed(title="⚠️ Changements des fichiers locaux ⚠️", color=ggr_utilities.ggr_orange)
			for d in diff:
				embed.add_field(name=typeDiff[d.change_type]["emoji"] + " " + typeDiff[d.change_type]["text"], value=d.a_blob.path, inline=False)
		await ctx.send(embed=embed)

	######################### SHELL COMMANDS #########################

	@Com.add_method(Com.Shell)
	def do_version(arg):
		'Return the verion hash number'
		sha = Utils.gitVerisonRoutine()
		ggr_utilities.logger("Git version: " + colored(sha, 'blue'), self)
		
	@Com.add_method(Com.Shell)
	def do_diff(arg):
		'Return the change in the local file system'
		diff = Utils.gitDiffRoutine()
		if (not diff):
			print(colored("Aucun changements locaux", 'green', attrs=['bold']))
		else:
			print(colored("Changements des fichiers locaux :", 'yellow', attrs=['bold']))
			for d in diff:
				print(colored(d.change_type, typeDiff[d.change_type]["color"], attrs=['bold']) + " : " + typeDiff[d.change_type]["text"] + " " + d.a_blob.path)

	############################ ROUTINES ############################
	
	@classmethod
	def gitVerisonRoutine(self):
		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		return(sha)

	@classmethod
	def gitDiffRoutine(self):
		repo = git.Repo(search_parent_directories=True)
		diff = repo.index.diff(None)
		return(diff)

def setup(bot):
	bot.add_cog(Utils(bot))