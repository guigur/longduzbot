import discord
from discord.ext import commands
import ggr_utilities, Database, Eco
import sqlite3
import os, sys

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.database = self.bot.get_cog('Database')
		if self.database is None:
			ggr_utilities.logger("Missing Database Cog", self, ggr_utilities.LogType.CRIT)

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " Cog Unloaded!" , self, None, ggr_utilities.LogType.WARN)

	# @commands.command()
	# @ggr_utilities.check_admin()
	# async def stop(self, ctx, arg = None):
	# 	'Stop the server'
	# 	ggr_utilities.logger("Stoping server", self)

	@commands.command()
	@ggr_utilities.check_admin()
	async def restart(self, ctx, arg = None):
		"""Restart the server"""
		ggr_utilities.logger("Restarting server", self)
		os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

	@commands.command()
	@ggr_utilities.check_admin()
	async def say(self, ctx, arg = None):
		"""say something in the channel"""
		if arg:
			ggr_utilities.logger("say " + ctx.message.content, self)
			await(ctx.send(ctx.message.content.split(' ', 1)[1]))
		await ctx.message.delete()

	@commands.command()
	@ggr_utilities.check_admin()
	async def resetArmy(self, ctx, arg = None):
		"""Reset the Maitre and Jeanfoutre"""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		await ggr_utilities.sudemote(ctx, role_meta="master")
		await ggr_utilities.sudemote(ctx, role_meta="worst")
		self.database.setDBArchiveMaitreJeanfoutre(Database.MaitreJeanfoutreType.MAITRE)
		self.database.setDBArchiveMaitreJeanfoutre(Database.MaitreJeanfoutreType.JEANFOUTRE)
		ggr_utilities.logger("The maitre and the jean foutre have been reseted.", self, ctx)
		await ctx.send("Le maitre et le jean foutre ont été réinitialisés.")

	@commands.command()
	@ggr_utilities.check_admin()
	async def giveWad(self, ctx, arg1 = None, arg2 = None):
		"""Give Wad to user or self"""
		ggr_utilities.logger(ctx.message.content, self, ctx)
		if arg1:
			if (arg1 and arg2):
				user = await commands.UserConverter().convert(ctx, str(arg1))
				moneyAmount = int(arg2)
			elif arg1:
				user = ctx.author
				moneyAmount = int(arg1)
			self.database.changeDBBalanceMoney(user, ctx.guild, moneyAmount)
			ggr_utilities.logger("The account of " + user.name + " " +  Eco.moneyGainEn(moneyAmount) + " " + str(abs(moneyAmount)) + " " + Eco.moneyName(moneyAmount) + "." , self, ctx)
			await ctx.send("Le compte de " + user.mention + " " +  Eco.moneyGain(moneyAmount) + " " + str(abs(moneyAmount)) + " " + Eco.moneyName(moneyAmount) + ".")

	@restart.error
	@say.error
	@resetArmy.error
	@giveWad.error
	async def not_admin_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			ggr_utilities.logger("User " + ctx.author.name + " tried to use a forbidden command!", self, ctx)
			await ctx.send("Vous n’avez pas accès à cette commande !")

def setup(bot):
	bot.add_cog(Admin(bot))